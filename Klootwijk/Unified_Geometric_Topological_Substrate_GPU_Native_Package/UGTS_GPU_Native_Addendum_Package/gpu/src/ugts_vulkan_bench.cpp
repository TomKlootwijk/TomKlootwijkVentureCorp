#include "ugts_vulkan_min.h"

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;
using Clock = std::chrono::steady_clock;

namespace {

void check(VkResult result, const char* what) {
    if (result != VK_SUCCESS) {
        throw std::runtime_error(std::string(what) + " failed with VkResult " + std::to_string(int(result)));
    }
}

double elapsed_ms(Clock::time_point a, Clock::time_point b) {
    return std::chrono::duration<double, std::milli>(b - a).count();
}

double percentile(std::vector<double> values, double q) {
    if (values.empty()) return 0.0;
    std::sort(values.begin(), values.end());
    const double x = q * double(values.size() - 1);
    const std::size_t lo = std::size_t(std::floor(x));
    const std::size_t hi = std::size_t(std::ceil(x));
    const double t = x - double(lo);
    return values[lo] * (1.0 - t) + values[hi] * t;
}

std::string json_escape(const std::string& s) {
    std::ostringstream out;
    for (unsigned char c : s) {
        switch (c) {
            case '\\': out << "\\\\"; break;
            case '"': out << "\\\""; break;
            case '\n': out << "\\n"; break;
            case '\r': out << "\\r"; break;
            case '\t': out << "\\t"; break;
            default:
                if (c < 0x20) out << "\\u" << std::hex << std::setw(4) << std::setfill('0') << int(c) << std::dec;
                else out << c;
        }
    }
    return out.str();
}

std::vector<std::uint32_t> read_spirv(const fs::path& path) {
    std::ifstream f(path, std::ios::binary | std::ios::ate);
    if (!f) throw std::runtime_error("cannot read SPIR-V: " + path.string());
    const auto size = f.tellg();
    if (size <= 0 || (std::uint64_t(size) % 4) != 0) throw std::runtime_error("invalid SPIR-V size");
    std::vector<std::uint32_t> words(std::size_t(size) / 4);
    f.seekg(0);
    f.read(reinterpret_cast<char*>(words.data()), size);
    if (!f || words.empty() || words[0] != 0x07230203u) throw std::runtime_error("invalid SPIR-V magic");
    return words;
}

void write_bytes(const fs::path& path, const std::vector<std::uint8_t>& data) {
    fs::create_directories(path.parent_path());
    std::ofstream f(path, std::ios::binary);
    if (!f) throw std::runtime_error("cannot write " + path.string());
    f.write(reinterpret_cast<const char*>(data.data()), std::streamsize(data.size()));
}

struct Args {
    fs::path spirv_dir = "spirv";
    fs::path out_dir = "vulkan_benchmark_out";
    std::vector<std::size_t> sizes = {1024, 16384, 262144, 1048576};
    int warmup = 3;
    int iterations = 12;
};

std::vector<std::size_t> parse_sizes(const std::string& text) {
    std::stringstream ss(text);
    std::string part;
    std::vector<std::size_t> out;
    while (std::getline(ss, part, ',')) if (!part.empty()) out.push_back(std::stoull(part));
    if (out.empty()) throw std::runtime_error("empty --sizes");
    return out;
}

Args parse_args(int argc, char** argv) {
    Args a;
    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        auto value = [&](const char* name) {
            if (i + 1 >= argc) throw std::runtime_error(std::string("missing value for ") + name);
            return std::string(argv[++i]);
        };
        if (arg == "--spirv-dir") a.spirv_dir = value("--spirv-dir");
        else if (arg == "--out-dir") a.out_dir = value("--out-dir");
        else if (arg == "--sizes") a.sizes = parse_sizes(value("--sizes"));
        else if (arg == "--warmup") a.warmup = std::stoi(value("--warmup"));
        else if (arg == "--iterations") a.iterations = std::stoi(value("--iterations"));
        else if (arg == "--help" || arg == "-h") {
            std::cout << "UGTS native Vulkan benchmark\n"
                      << "  --spirv-dir PATH\n  --out-dir PATH\n  --sizes N,N,...\n"
                      << "  --warmup N\n  --iterations N\n";
            std::exit(0);
        } else throw std::runtime_error("unknown argument: " + arg);
    }
    if (a.warmup < 0 || a.iterations < 1) throw std::runtime_error("invalid iteration count");
    return a;
}

std::uint32_t api_major(std::uint32_t v) { return (v >> 22u) & 0x7fu; }
std::uint32_t api_minor(std::uint32_t v) { return (v >> 12u) & 0x3ffu; }
std::uint32_t api_patch(std::uint32_t v) { return v & 0xfffu; }

class VulkanContext {
public:
    VulkanContext() {
        VkApplicationInfo app{};
        app.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
        app.pApplicationName = "UGTS Native Substrate Benchmark";
        app.applicationVersion = 1;
        app.pEngineName = "UGTS-GN";
        app.engineVersion = 1;
        app.apiVersion = VK_API_VERSION_1_1;

        VkInstanceCreateInfo ici{};
        ici.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
        ici.pApplicationInfo = &app;
        VkResult ir = vkCreateInstance(&ici, nullptr, &instance_);
        if (ir == VK_ERROR_INCOMPATIBLE_DRIVER) {
            app.apiVersion = VK_API_VERSION_1_0;
            check(vkCreateInstance(&ici, nullptr, &instance_), "vkCreateInstance(1.0)");
        } else check(ir, "vkCreateInstance");

        std::uint32_t count = 0;
        check(vkEnumeratePhysicalDevices(instance_, &count, nullptr), "vkEnumeratePhysicalDevices(count)");
        if (!count) throw std::runtime_error("no Vulkan physical devices");
        std::vector<VkPhysicalDevice> devices(count);
        check(vkEnumeratePhysicalDevices(instance_, &count, devices.data()), "vkEnumeratePhysicalDevices(list)");

        // Prefer a discrete/integrated/virtual GPU; fall back to CPU (SwiftShader in this validation container).
        physical_ = devices.front();
        int best_rank = -1;
        for (auto d : devices) {
            VkPhysicalDeviceProperties p{};
            vkGetPhysicalDeviceProperties(d, &p);
            int rank = 0;
            if (p.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU) rank = 4;
            else if (p.deviceType == VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU) rank = 3;
            else if (p.deviceType == VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU) rank = 2;
            else if (p.deviceType == VK_PHYSICAL_DEVICE_TYPE_CPU) rank = 1;
            if (rank > best_rank) { best_rank = rank; physical_ = d; props_ = p; }
        }

        std::uint32_t qcount = 0;
        vkGetPhysicalDeviceQueueFamilyProperties(physical_, &qcount, nullptr);
        std::vector<VkQueueFamilyProperties> qprops(qcount);
        vkGetPhysicalDeviceQueueFamilyProperties(physical_, &qcount, qprops.data());
        bool found = false;
        for (std::uint32_t i = 0; i < qcount; ++i) {
            if (qprops[i].queueCount && (qprops[i].queueFlags & VK_QUEUE_COMPUTE_BIT)) {
                queue_family_ = i;
                timestamp_bits_ = qprops[i].timestampValidBits;
                found = true;
                break;
            }
        }
        if (!found) throw std::runtime_error("no compute queue family");

        const float priority = 1.0f;
        VkDeviceQueueCreateInfo qci{};
        qci.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
        qci.queueFamilyIndex = queue_family_;
        qci.queueCount = 1;
        qci.pQueuePriorities = &priority;
        VkDeviceCreateInfo dci{};
        dci.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
        dci.queueCreateInfoCount = 1;
        dci.pQueueCreateInfos = &qci;
        check(vkCreateDevice(physical_, &dci, nullptr, &device_), "vkCreateDevice");
        vkGetDeviceQueue(device_, queue_family_, 0, &queue_);
        vkGetPhysicalDeviceMemoryProperties(physical_, &mem_props_);

        VkCommandPoolCreateInfo cpci{};
        cpci.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
        cpci.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
        cpci.queueFamilyIndex = queue_family_;
        check(vkCreateCommandPool(device_, &cpci, nullptr, &command_pool_), "vkCreateCommandPool");
    }

    ~VulkanContext() {
        if (device_) {
            vkDeviceWaitIdle(device_);
            if (command_pool_) vkDestroyCommandPool(device_, command_pool_, nullptr);
            vkDestroyDevice(device_, nullptr);
        }
        if (instance_) vkDestroyInstance(instance_, nullptr);
    }

    std::uint32_t find_memory_type(std::uint32_t bits, VkMemoryPropertyFlags required) const {
        for (std::uint32_t i = 0; i < mem_props_.memoryTypeCount; ++i) {
            if ((bits & (1u << i)) && (mem_props_.memoryTypes[i].propertyFlags & required) == required) return i;
        }
        throw std::runtime_error("no compatible host-visible coherent memory type");
    }

    VkDevice device() const { return device_; }
    VkPhysicalDevice physical() const { return physical_; }
    VkQueue queue() const { return queue_; }
    VkCommandPool command_pool() const { return command_pool_; }
    const VkPhysicalDeviceProperties& properties() const { return props_; }
    std::uint32_t queue_family() const { return queue_family_; }
    std::uint32_t timestamp_bits() const { return timestamp_bits_; }
    float timestamp_period_ns() const { return props_.limits.timestampPeriod; }

private:
    VkInstance instance_ = VK_NULL_HANDLE;
    VkPhysicalDevice physical_ = VK_NULL_HANDLE;
    VkDevice device_ = VK_NULL_HANDLE;
    VkQueue queue_ = VK_NULL_HANDLE;
    VkCommandPool command_pool_ = VK_NULL_HANDLE;
    VkPhysicalDeviceProperties props_{};
    VkPhysicalDeviceMemoryProperties mem_props_{};
    std::uint32_t queue_family_ = 0;
    std::uint32_t timestamp_bits_ = 0;
};

struct MappedBuffer {
    const VulkanContext* ctx = nullptr;
    VkBuffer buffer = VK_NULL_HANDLE;
    VkDeviceMemory memory = VK_NULL_HANDLE;
    VkDeviceSize size = 0;
    void* mapped = nullptr;

    MappedBuffer() = default;
    MappedBuffer(const VulkanContext& c, VkDeviceSize bytes) : ctx(&c), size(bytes) {
        VkBufferCreateInfo bci{};
        bci.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
        bci.size = bytes;
        bci.usage = VK_BUFFER_USAGE_STORAGE_BUFFER_BIT;
        bci.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
        check(vkCreateBuffer(c.device(), &bci, nullptr, &buffer), "vkCreateBuffer");
        VkMemoryRequirements req{};
        vkGetBufferMemoryRequirements(c.device(), buffer, &req);
        VkMemoryAllocateInfo mai{};
        mai.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
        mai.allocationSize = req.size;
        mai.memoryTypeIndex = c.find_memory_type(req.memoryTypeBits,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT);
        check(vkAllocateMemory(c.device(), &mai, nullptr, &memory), "vkAllocateMemory");
        check(vkBindBufferMemory(c.device(), buffer, memory, 0), "vkBindBufferMemory");
        check(vkMapMemory(c.device(), memory, 0, bytes, 0, &mapped), "vkMapMemory");
    }

    MappedBuffer(const MappedBuffer&) = delete;
    MappedBuffer& operator=(const MappedBuffer&) = delete;
    MappedBuffer(MappedBuffer&& other) noexcept { *this = std::move(other); }
    MappedBuffer& operator=(MappedBuffer&& other) noexcept {
        if (this != &other) {
            release();
            ctx = other.ctx; buffer = other.buffer; memory = other.memory; size = other.size; mapped = other.mapped;
            other.ctx = nullptr; other.buffer = VK_NULL_HANDLE; other.memory = VK_NULL_HANDLE; other.mapped = nullptr; other.size = 0;
        }
        return *this;
    }
    ~MappedBuffer() { release(); }

    void release() {
        if (!ctx) return;
        if (mapped) vkUnmapMemory(ctx->device(), memory);
        if (buffer) vkDestroyBuffer(ctx->device(), buffer, nullptr);
        if (memory) vkFreeMemory(ctx->device(), memory, nullptr);
        ctx = nullptr; buffer = VK_NULL_HANDLE; memory = VK_NULL_HANDLE; mapped = nullptr; size = 0;
    }
};

std::uint32_t mix32(std::uint32_t x) {
    x ^= x >> 16; x *= 0x7feb352du; x ^= x >> 15; x *= 0x846ca68bu; x ^= x >> 16; return x;
}

std::uint16_t f32_to_f16(float f) {
    std::uint32_t x; std::memcpy(&x, &f, 4);
    const std::uint32_t sign = (x >> 16) & 0x8000u;
    int exp = int((x >> 23) & 0xffu) - 127 + 15;
    std::uint32_t mant = x & 0x7fffffu;
    if (exp <= 0) {
        if (exp < -10) return std::uint16_t(sign);
        mant = (mant | 0x800000u) >> (1 - exp);
        return std::uint16_t(sign | ((mant + 0x1000u) >> 13));
    }
    if (exp >= 31) return std::uint16_t(sign | 0x7c00u);
    return std::uint16_t(sign | (std::uint32_t(exp) << 10) | ((mant + 0x1000u) >> 13));
}

float f16_to_f32(std::uint16_t h) {
    const std::uint32_t sign = std::uint32_t(h & 0x8000u) << 16;
    std::uint32_t exp = (h >> 10) & 0x1fu;
    std::uint32_t mant = h & 0x3ffu;
    std::uint32_t x;
    if (exp == 0) {
        if (!mant) x = sign;
        else {
            exp = 1;
            while (!(mant & 0x400u)) { mant <<= 1; --exp; }
            mant &= 0x3ffu;
            x = sign | ((exp + 112u) << 23) | (mant << 13);
        }
    } else if (exp == 31) x = sign | 0x7f800000u | (mant << 13);
    else x = sign | ((exp + 112u) << 23) | (mant << 13);
    float f; std::memcpy(&f, &x, 4); return f;
}

std::uint32_t pack2(float a, float b) { return std::uint32_t(f32_to_f16(a)) | (std::uint32_t(f32_to_f16(b)) << 16); }
std::array<float,2> unpack2(std::uint32_t x) { return {f16_to_f32(std::uint16_t(x)), f16_to_f32(std::uint16_t(x >> 16))}; }

struct alignas(16) State64 { float position_time[4], axis_radius[4], phase_guard[4]; std::uint32_t meta[4]; };
struct alignas(16) Event32 { std::uint32_t scalar_bits[4], topology_bits[4]; };
struct alignas(16) State32 { std::uint32_t words[8]; };
struct alignas(16) Event16 { std::uint32_t words[4]; };
static_assert(sizeof(State64) == 64 && sizeof(Event32) == 32 && sizeof(State32) == 32 && sizeof(Event16) == 16);

struct Fields {
    float px,py,pz,time, ax,ay,az,radius, cone_cos,phase,guard_epsilon,confidence_floor;
    std::uint32_t sheet,orientation,compatibility_mask,lineage_seed;
};

Fields fields_for(std::size_t i) {
    const float a = float(i % 1024) * 0.01f;
    const float r = 10.0f + float(int(i % 17) - 8) * 0.002f;
    Fields f{};
    f.px=r*std::cos(a);f.py=r*std::sin(a);f.pz=0;f.time=float(i)*0.001f;
    f.ax=std::cos(a);f.ay=std::sin(a);f.az=0;f.radius=10;
    f.cone_cos=0.5f;f.phase=float(i%256)/256.0f;f.guard_epsilon=0.010f;f.confidence_floor=0.70f;
    f.sheet=std::uint32_t(i&1u);f.orientation=std::uint32_t((i>>1u)&1u);
    f.compatibility_mask=(i%3)?4u:1u;f.lineage_seed=std::uint32_t(i*2654435761u);
    return f;
}

State64 make64(std::size_t i) {
    const auto f=fields_for(i); State64 s{};
    s.position_time[0]=f.px;s.position_time[1]=f.py;s.position_time[2]=f.pz;s.position_time[3]=f.time;
    s.axis_radius[0]=f.ax;s.axis_radius[1]=f.ay;s.axis_radius[2]=f.az;s.axis_radius[3]=f.radius;
    s.phase_guard[0]=f.cone_cos;s.phase_guard[1]=f.phase;s.phase_guard[2]=f.guard_epsilon;s.phase_guard[3]=f.confidence_floor;
    s.meta[0]=f.sheet;s.meta[1]=f.orientation;s.meta[2]=f.compatibility_mask;s.meta[3]=f.lineage_seed; return s;
}

State32 make32(std::size_t i) {
    const auto f=fields_for(i); State32 s{};
    s.words[0]=pack2(f.px,f.py);s.words[1]=pack2(f.pz,f.time);s.words[2]=pack2(f.ax,f.ay);s.words[3]=pack2(f.az,f.radius);
    s.words[4]=pack2(f.cone_cos,f.phase);s.words[5]=pack2(f.guard_epsilon,f.confidence_floor);
    s.words[6]=f.sheet|(f.orientation<<8)|((f.compatibility_mask&0xffffu)<<9);s.words[7]=f.lineage_seed; return s;
}

Fields decode32(const State32& s) {
    auto xy=unpack2(s.words[0]),zt=unpack2(s.words[1]),aa=unpack2(s.words[2]),ar=unpack2(s.words[3]),cp=unpack2(s.words[4]),gc=unpack2(s.words[5]);
    Fields f{};f.px=xy[0];f.py=xy[1];f.pz=zt[0];f.time=zt[1];f.ax=aa[0];f.ay=aa[1];f.az=ar[0];f.radius=ar[1];
    f.cone_cos=cp[0];f.phase=cp[1];f.guard_epsilon=gc[0];f.confidence_floor=gc[1];
    f.sheet=s.words[6]&255u;f.orientation=(s.words[6]>>8)&1u;f.compatibility_mask=(s.words[6]>>9)&0xffffu;f.lineage_seed=s.words[7];return f;
}

struct Eval { bool support=false,compatible=false,verified=false; std::uint32_t route=0,lineage=0; };
Eval eval(const Fields& f,std::size_t i) {
    Eval e{};const float r=std::sqrt(f.px*f.px+f.py*f.py+f.pz*f.pz);const float al=std::sqrt(f.ax*f.ax+f.ay*f.ay+f.az*f.az);
    const float c=(r>1e-8f&&al>1e-8f)?(f.px*f.ax+f.py*f.ay+f.pz*f.az)/(r*al):1.0f;
    e.support=r<=f.radius&&c>=f.cone_cos;e.compatible=(f.compatibility_mask&4u)&&f.sheet==1u&&(f.orientation&1u)==0u;
    const float sdf=r-f.radius,guard=std::abs(sdf)-f.guard_epsilon,confidence=std::exp2(-std::abs(sdf)*32.0f);
    e.verified=e.support&&e.compatible&&guard<=0&&confidence>=f.confidence_floor;e.route=(f.orientation^(e.verified?1u:0u))&1u;e.lineage=mix32(f.lineage_seed^std::uint32_t(i));return e;
}

struct Counts { std::uint64_t candidates=0,supported=0,compatible=0,verified=0; };
template<class T,class Decode> Counts counts_for(const std::vector<T>& states,Decode decode) {
    Counts c{};for(std::size_t i=0;i<states.size();++i){auto e=eval(decode(states[i]),i);++c.candidates;if(e.support)++c.supported;if(e.support&&e.compatible)++c.compatible;if(e.verified)++c.verified;}return c;
}

struct PipelineProgram {
    VkShaderModule module=VK_NULL_HANDLE;VkPipelineCache cache=VK_NULL_HANDLE;VkPipeline pipeline=VK_NULL_HANDLE;
    double module_create_ms=0,cold_pipeline_ms=0,cached_pipeline_ms=0;std::vector<std::uint8_t> cache_blob;bool cache_reload_ok=false;
};

PipelineProgram create_pipeline(const VulkanContext& ctx,VkPipelineLayout layout,const std::vector<std::uint32_t>& spv,const fs::path& cache_path) {
    PipelineProgram p{};
    VkShaderModuleCreateInfo sm{};sm.sType=VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;sm.codeSize=spv.size()*4;sm.pCode=spv.data();
    auto t0=Clock::now();check(vkCreateShaderModule(ctx.device(),&sm,nullptr,&p.module),"vkCreateShaderModule");auto t1=Clock::now();p.module_create_ms=elapsed_ms(t0,t1);
    VkPipelineCacheCreateInfo pci{};pci.sType=VK_STRUCTURE_TYPE_PIPELINE_CACHE_CREATE_INFO;check(vkCreatePipelineCache(ctx.device(),&pci,nullptr,&p.cache),"vkCreatePipelineCache");
    VkPipelineShaderStageCreateInfo stage{};stage.sType=VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;stage.stage=VK_SHADER_STAGE_COMPUTE_BIT;stage.module=p.module;stage.pName="main";
    VkComputePipelineCreateInfo ci{};ci.sType=VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO;ci.stage=stage;ci.layout=layout;
    t0=Clock::now();check(vkCreateComputePipelines(ctx.device(),p.cache,1,&ci,nullptr,&p.pipeline),"vkCreateComputePipelines(cold)");t1=Clock::now();p.cold_pipeline_ms=elapsed_ms(t0,t1);
    std::size_t bytes=0;check(vkGetPipelineCacheData(ctx.device(),p.cache,&bytes,nullptr),"vkGetPipelineCacheData(size)");p.cache_blob.resize(bytes);
    if(bytes){check(vkGetPipelineCacheData(ctx.device(),p.cache,&bytes,p.cache_blob.data()),"vkGetPipelineCacheData(data)");p.cache_blob.resize(bytes);write_bytes(cache_path,p.cache_blob);}
    vkDestroyPipeline(ctx.device(),p.pipeline,nullptr);p.pipeline=VK_NULL_HANDLE;vkDestroyPipelineCache(ctx.device(),p.cache,nullptr);p.cache=VK_NULL_HANDLE;
    VkPipelineCacheCreateInfo warm{};warm.sType=VK_STRUCTURE_TYPE_PIPELINE_CACHE_CREATE_INFO;warm.initialDataSize=p.cache_blob.size();warm.pInitialData=p.cache_blob.data();
    check(vkCreatePipelineCache(ctx.device(),&warm,nullptr,&p.cache),"vkCreatePipelineCache(reload)");
    t0=Clock::now();VkResult result=vkCreateComputePipelines(ctx.device(),p.cache,1,&ci,nullptr,&p.pipeline);t1=Clock::now();p.cached_pipeline_ms=elapsed_ms(t0,t1);p.cache_reload_ok=result==VK_SUCCESS;check(result,"vkCreateComputePipelines(cached)");return p;
}

void destroy_program(const VulkanContext& ctx,PipelineProgram& p){if(p.pipeline)vkDestroyPipeline(ctx.device(),p.pipeline,nullptr);if(p.cache)vkDestroyPipelineCache(ctx.device(),p.cache,nullptr);if(p.module)vkDestroyShaderModule(ctx.device(),p.module,nullptr);p={};}

struct BenchRow {
    std::string profile,mode;std::size_t candidates=0,input_record_bytes=0,output_record_bytes=0,total_buffer_bytes=0;
    double setup_ms=0,host_min_ms=0,host_mean_ms=0,host_p50_ms=0,host_p95_ms=0,host_p99_ms=0,host_max_ms=0;
    double device_min_ms=0,device_mean_ms=0,device_p50_ms=0,device_p95_ms=0,device_p99_ms=0,device_max_ms=0;
    double candidate_rate_mps=0,verified_event_rate_mps=0,effective_bandwidth_gbps=0;Counts counts{};bool counters_ok=false,sample_ok=false;
};

template<class StateT,class EventT,class Make,class Decode>
BenchRow run_one(const VulkanContext& ctx,VkDescriptorSetLayout dsl,VkPipelineLayout layout,VkPipeline pipeline,const std::string& profile,const std::string& mode,bool commit,std::size_t n,int warmup,int iterations,Make make,Decode decode) {
    auto setup0=Clock::now();
    std::vector<StateT> states(n);for(std::size_t i=0;i<n;++i)states[i]=make(i);const Counts expected=counts_for(states,decode);
    MappedBuffer input(ctx,n*sizeof(StateT)),output(ctx,n*sizeof(EventT)),counter(ctx,16);
    std::memcpy(input.mapped,states.data(),n*sizeof(StateT));std::memset(output.mapped,0,n*sizeof(EventT));std::memset(counter.mapped,0,16);
    VkDescriptorPoolSize ps{VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,3};VkDescriptorPoolCreateInfo dp{};dp.sType=VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;dp.maxSets=1;dp.poolSizeCount=1;dp.pPoolSizes=&ps;
    VkDescriptorPool pool=VK_NULL_HANDLE;check(vkCreateDescriptorPool(ctx.device(),&dp,nullptr,&pool),"vkCreateDescriptorPool");
    VkDescriptorSetAllocateInfo dai{};dai.sType=VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;dai.descriptorPool=pool;dai.descriptorSetCount=1;dai.pSetLayouts=&dsl;VkDescriptorSet set=VK_NULL_HANDLE;check(vkAllocateDescriptorSets(ctx.device(),&dai,&set),"vkAllocateDescriptorSets");
    VkDescriptorBufferInfo infos[3]={{input.buffer,0,input.size},{output.buffer,0,output.size},{counter.buffer,0,counter.size}};VkWriteDescriptorSet writes[3]{};
    for(std::uint32_t i=0;i<3;++i){writes[i].sType=VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;writes[i].dstSet=set;writes[i].dstBinding=i;writes[i].descriptorCount=1;writes[i].descriptorType=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER;writes[i].pBufferInfo=&infos[i];}
    vkUpdateDescriptorSets(ctx.device(),3,writes,0,nullptr);
    VkCommandBufferAllocateInfo cai{};cai.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;cai.commandPool=ctx.command_pool();cai.level=VK_COMMAND_BUFFER_LEVEL_PRIMARY;cai.commandBufferCount=1;VkCommandBuffer cmd=VK_NULL_HANDLE;check(vkAllocateCommandBuffers(ctx.device(),&cai,&cmd),"vkAllocateCommandBuffers");
    VkQueryPoolCreateInfo qci{};qci.sType=VK_STRUCTURE_TYPE_QUERY_POOL_CREATE_INFO;qci.queryType=VK_QUERY_TYPE_TIMESTAMP;qci.queryCount=2;VkQueryPool qp=VK_NULL_HANDLE;check(vkCreateQueryPool(ctx.device(),&qci,nullptr,&qp),"vkCreateQueryPool");
    VkCommandBufferBeginInfo bi{};bi.sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;bi.flags=VK_COMMAND_BUFFER_USAGE_SIMULTANEOUS_USE_BIT;check(vkBeginCommandBuffer(cmd,&bi),"vkBeginCommandBuffer");
    vkCmdResetQueryPool(cmd,qp,0,2);vkCmdWriteTimestamp(cmd,VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,qp,0);vkCmdBindPipeline(cmd,VK_PIPELINE_BIND_POINT_COMPUTE,pipeline);vkCmdBindDescriptorSets(cmd,VK_PIPELINE_BIND_POINT_COMPUTE,layout,0,1,&set,0,nullptr);vkCmdDispatch(cmd,std::uint32_t((n+255)/256),1,1);vkCmdWriteTimestamp(cmd,VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT,qp,1);
    VkBufferMemoryBarrier barriers[2]{};for(auto& b:barriers){b.sType=VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER;b.srcAccessMask=VK_ACCESS_SHADER_WRITE_BIT;b.dstAccessMask=VK_ACCESS_HOST_READ_BIT;b.srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED;b.dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED;b.offset=0;b.size=VK_WHOLE_SIZE;}barriers[0].buffer=output.buffer;barriers[1].buffer=counter.buffer;
    vkCmdPipelineBarrier(cmd,VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,VK_PIPELINE_STAGE_HOST_BIT,0,0,nullptr,2,barriers,0,nullptr);check(vkEndCommandBuffer(cmd),"vkEndCommandBuffer");
    VkFenceCreateInfo fci{};fci.sType=VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;VkFence fence=VK_NULL_HANDLE;check(vkCreateFence(ctx.device(),&fci,nullptr,&fence),"vkCreateFence");
    VkSubmitInfo si{};si.sType=VK_STRUCTURE_TYPE_SUBMIT_INFO;si.commandBufferCount=1;si.pCommandBuffers=&cmd;
    auto setup1=Clock::now();
    auto submit=[&](double* host,double* device){std::memset(counter.mapped,0,16);check(vkResetFences(ctx.device(),1,&fence),"vkResetFences");auto a=Clock::now();check(vkQueueSubmit(ctx.queue(),1,&si,fence),"vkQueueSubmit");check(vkWaitForFences(ctx.device(),1,&fence,VK_TRUE,std::numeric_limits<std::uint64_t>::max()),"vkWaitForFences");auto b=Clock::now();if(host)*host=elapsed_ms(a,b);std::uint64_t ticks[2]={};check(vkGetQueryPoolResults(ctx.device(),qp,0,2,sizeof(ticks),ticks,sizeof(std::uint64_t),VK_QUERY_RESULT_64_BIT|VK_QUERY_RESULT_WAIT_BIT),"vkGetQueryPoolResults");std::uint64_t delta=0;if(ctx.timestamp_bits()>=64)delta=ticks[1]-ticks[0];else if(ctx.timestamp_bits()>0){const std::uint64_t mask=(std::uint64_t(1)<<ctx.timestamp_bits())-1;delta=(ticks[1]-ticks[0])&mask;}if(device)*device=double(delta)*double(ctx.timestamp_period_ns())/1.0e6;};
    for(int i=0;i<warmup;++i)submit(nullptr,nullptr);
    std::vector<double> host_times,device_times;host_times.reserve(iterations);device_times.reserve(iterations);for(int i=0;i<iterations;++i){double h=0,d=0;submit(&h,&d);host_times.push_back(h);device_times.push_back(d);}
    const auto* actual32=static_cast<const std::uint32_t*>(counter.mapped);Counts actual=expected;bool counters_ok=!commit;if(commit){actual={actual32[0],actual32[1],actual32[2],actual32[3]};counters_ok=actual.candidates==expected.candidates&&actual.supported==expected.supported&&actual.compatible==expected.compatible&&actual.verified==expected.verified;}
    bool sample_ok=true;const std::size_t sample=std::min<std::size_t>(n,4096);const EventT* events=static_cast<const EventT*>(output.mapped);for(std::size_t i=0;i<sample;++i){const auto e=eval(decode(states[i]),i);std::uint32_t verified,route,lineage;if constexpr(sizeof(EventT)==32){verified=events[i].topology_bits[0];route=events[i].topology_bits[1];lineage=events[i].topology_bits[2];}else{verified=events[i].words[2]&1u;route=(events[i].words[2]>>1)&1u;lineage=events[i].words[3];}if(verified!=(e.verified?1u:0u)||route!=e.route||lineage!=e.lineage){sample_ok=false;break;}}
    BenchRow r{};r.profile=profile;r.mode=mode;r.candidates=n;r.input_record_bytes=sizeof(StateT);r.output_record_bytes=sizeof(EventT);r.total_buffer_bytes=n*(sizeof(StateT)+sizeof(EventT))+16;r.setup_ms=elapsed_ms(setup0,setup1);
    r.host_min_ms=*std::min_element(host_times.begin(),host_times.end());r.host_max_ms=*std::max_element(host_times.begin(),host_times.end());r.host_mean_ms=std::accumulate(host_times.begin(),host_times.end(),0.0)/host_times.size();r.host_p50_ms=percentile(host_times,.5);r.host_p95_ms=percentile(host_times,.95);r.host_p99_ms=percentile(host_times,.99);
    r.device_min_ms=*std::min_element(device_times.begin(),device_times.end());r.device_max_ms=*std::max_element(device_times.begin(),device_times.end());r.device_mean_ms=std::accumulate(device_times.begin(),device_times.end(),0.0)/device_times.size();r.device_p50_ms=percentile(device_times,.5);r.device_p95_ms=percentile(device_times,.95);r.device_p99_ms=percentile(device_times,.99);
    const double basis=r.device_p50_ms>0?r.device_p50_ms:r.host_p50_ms;r.candidate_rate_mps=double(n)/basis/1000.0;r.verified_event_rate_mps=double(actual.verified)/basis/1000.0;r.effective_bandwidth_gbps=double(n*(sizeof(StateT)+sizeof(EventT)))/(basis*1e6);r.counts=actual;r.counters_ok=counters_ok;r.sample_ok=sample_ok;
    vkDestroyFence(ctx.device(),fence,nullptr);vkDestroyQueryPool(ctx.device(),qp,nullptr);vkDestroyDescriptorPool(ctx.device(),pool,nullptr);return r;
}

struct ProgramRecord {std::string name;fs::path spv_path;PipelineProgram program;};

void write_json(const VulkanContext& ctx,const Args& args,const std::vector<ProgramRecord>& programs,const std::vector<BenchRow>& rows,const fs::path& path){std::ofstream f(path);f<<std::fixed<<std::setprecision(6);const auto&p=ctx.properties();f<<"{\n  \"schema\": \"UGTS-VK-BENCH-1.1\",\n  \"runtime\": \"Vulkan compute\",\n  \"physical_gpu_claim\": "<<(p.deviceType==VK_PHYSICAL_DEVICE_TYPE_CPU?"false":"true")<<",\n  \"device\": {\"name\": \""<<json_escape(p.deviceName)<<"\", \"type\": "<<int(p.deviceType)<<", \"vendor_id\": "<<p.vendorID<<", \"device_id\": "<<p.deviceID<<", \"api_version\": \""<<api_major(p.apiVersion)<<'.'<<api_minor(p.apiVersion)<<'.'<<api_patch(p.apiVersion)<<"\", \"timestamp_period_ns\": "<<p.limits.timestampPeriod<<", \"timestamp_valid_bits\": "<<ctx.timestamp_bits()<<"},\n  \"run_parameters\": {\"warmup\": "<<args.warmup<<", \"iterations\": "<<args.iterations<<"},\n  \"programs\": [\n";for(std::size_t i=0;i<programs.size();++i){const auto&x=programs[i];f<<"    {\"name\": \""<<x.name<<"\", \"spirv_bytes\": "<<fs::file_size(x.spv_path)<<", \"shader_module_create_ms\": "<<x.program.module_create_ms<<", \"cold_pipeline_create_ms\": "<<x.program.cold_pipeline_ms<<", \"pipeline_cache_bytes\": "<<x.program.cache_blob.size()<<", \"cached_pipeline_create_ms\": "<<x.program.cached_pipeline_ms<<", \"cache_reload_ok\": "<<(x.program.cache_reload_ok?"true":"false")<<"}"<<(i+1==programs.size()?"\n":",\n");}f<<"  ],\n  \"benchmarks\": [\n";for(std::size_t i=0;i<rows.size();++i){const auto&r=rows[i];f<<"    {\"profile\": \""<<r.profile<<"\", \"mode\": \""<<r.mode<<"\", \"candidates\": "<<r.candidates<<", \"input_record_bytes\": "<<r.input_record_bytes<<", \"output_record_bytes\": "<<r.output_record_bytes<<", \"total_buffer_bytes\": "<<r.total_buffer_bytes<<", \"setup_ms\": "<<r.setup_ms<<", \"host_dispatch_ms\": {\"min\": "<<r.host_min_ms<<", \"mean\": "<<r.host_mean_ms<<", \"p50\": "<<r.host_p50_ms<<", \"p95\": "<<r.host_p95_ms<<", \"p99\": "<<r.host_p99_ms<<", \"max\": "<<r.host_max_ms<<"}, \"device_dispatch_ms\": {\"min\": "<<r.device_min_ms<<", \"mean\": "<<r.device_mean_ms<<", \"p50\": "<<r.device_p50_ms<<", \"p95\": "<<r.device_p95_ms<<", \"p99\": "<<r.device_p99_ms<<", \"max\": "<<r.device_max_ms<<"}, \"candidate_rate_mps\": "<<r.candidate_rate_mps<<", \"verified_event_rate_mps\": "<<r.verified_event_rate_mps<<", \"effective_bandwidth_gbps\": "<<r.effective_bandwidth_gbps<<", \"counts\": {\"candidates\": "<<r.counts.candidates<<", \"supported\": "<<r.counts.supported<<", \"compatible\": "<<r.counts.compatible<<", \"verified\": "<<r.counts.verified<<"}, \"counter_validation\": "<<(r.counters_ok?"true":"false")<<", \"sample_validation\": "<<(r.sample_ok?"true":"false")<<"}"<<(i+1==rows.size()?"\n":",\n");}f<<"  ]\n}\n";}

void write_csv(const std::vector<BenchRow>& rows,const fs::path& path){std::ofstream f(path);f<<"profile,mode,candidates,input_record_bytes,output_record_bytes,total_buffer_bytes,setup_ms,host_p50_ms,host_p95_ms,host_p99_ms,device_p50_ms,device_p95_ms,device_p99_ms,candidate_rate_mps,verified_event_rate_mps,effective_bandwidth_gbps,supported,compatible,verified,counter_validation,sample_validation\n"<<std::fixed<<std::setprecision(6);for(const auto&r:rows)f<<r.profile<<','<<r.mode<<','<<r.candidates<<','<<r.input_record_bytes<<','<<r.output_record_bytes<<','<<r.total_buffer_bytes<<','<<r.setup_ms<<','<<r.host_p50_ms<<','<<r.host_p95_ms<<','<<r.host_p99_ms<<','<<r.device_p50_ms<<','<<r.device_p95_ms<<','<<r.device_p99_ms<<','<<r.candidate_rate_mps<<','<<r.verified_event_rate_mps<<','<<r.effective_bandwidth_gbps<<','<<r.counts.supported<<','<<r.counts.compatible<<','<<r.counts.verified<<','<<(r.counters_ok?1:0)<<','<<(r.sample_ok?1:0)<<'\n';}

} // namespace

int main(int argc,char**argv){try{const Args args=parse_args(argc,argv);fs::create_directories(args.out_dir/"pipeline_cache");VulkanContext ctx;const auto&props=ctx.properties();std::cout<<"Vulkan device: "<<props.deviceName<<" | API "<<api_major(props.apiVersion)<<'.'<<api_minor(props.apiVersion)<<'.'<<api_patch(props.apiVersion)<<" | timestamp "<<props.limits.timestampPeriod<<" ns\n";
    VkDescriptorSetLayoutBinding bindings[3]{};for(std::uint32_t i=0;i<3;++i){bindings[i].binding=i;bindings[i].descriptorType=VK_DESCRIPTOR_TYPE_STORAGE_BUFFER;bindings[i].descriptorCount=1;bindings[i].stageFlags=VK_SHADER_STAGE_COMPUTE_BIT;}VkDescriptorSetLayoutCreateInfo dci{};dci.sType=VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;dci.bindingCount=3;dci.pBindings=bindings;VkDescriptorSetLayout dsl=VK_NULL_HANDLE;check(vkCreateDescriptorSetLayout(ctx.device(),&dci,nullptr,&dsl),"vkCreateDescriptorSetLayout");VkPipelineLayoutCreateInfo plci{};plci.sType=VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;plci.setLayoutCount=1;plci.pSetLayouts=&dsl;VkPipelineLayout layout=VK_NULL_HANDLE;check(vkCreatePipelineLayout(ctx.device(),&plci,nullptr,&layout),"vkCreatePipelineLayout");
    struct Job{std::string profile,mode,file;bool commit;};std::vector<Job>jobs={{"G64_E32","evaluate","ugts_g64_evaluate.spv",false},{"G64_E32","evaluate_commit","ugts_g64_evaluate_commit.spv",true},{"G32_E16","evaluate","ugts_g32_evaluate.spv",false},{"G32_E16","evaluate_commit","ugts_g32_evaluate_commit.spv",true}};std::vector<ProgramRecord>programs;std::vector<BenchRow>rows;
    for(const auto&j:jobs){ProgramRecord pr{};pr.name=j.profile+"_"+j.mode;pr.spv_path=args.spirv_dir/j.file;auto spv=read_spirv(pr.spv_path);std::cout<<"Creating pipeline "<<pr.name<<"...\n";pr.program=create_pipeline(ctx,layout,spv,args.out_dir/"pipeline_cache"/(pr.name+".vkcache"));for(auto n:args.sizes){BenchRow r;if(j.profile=="G64_E32")r=run_one<State64,Event32>(ctx,dsl,layout,pr.program.pipeline,j.profile,j.mode,j.commit,n,args.warmup,args.iterations,make64,[](const State64&s){Fields f{};f.px=s.position_time[0];f.py=s.position_time[1];f.pz=s.position_time[2];f.time=s.position_time[3];f.ax=s.axis_radius[0];f.ay=s.axis_radius[1];f.az=s.axis_radius[2];f.radius=s.axis_radius[3];f.cone_cos=s.phase_guard[0];f.phase=s.phase_guard[1];f.guard_epsilon=s.phase_guard[2];f.confidence_floor=s.phase_guard[3];f.sheet=s.meta[0];f.orientation=s.meta[1];f.compatibility_mask=s.meta[2];f.lineage_seed=s.meta[3];return f;});else r=run_one<State32,Event16>(ctx,dsl,layout,pr.program.pipeline,j.profile,j.mode,j.commit,n,args.warmup,args.iterations,make32,decode32);std::cout<<"  N="<<n<<" device-p50="<<std::fixed<<std::setprecision(3)<<r.device_p50_ms<<" ms host-p50="<<r.host_p50_ms<<" ms CER="<<std::setprecision(2)<<r.candidate_rate_mps<<" M/s SET="<<r.verified_event_rate_mps<<" M/s valid="<<(r.sample_ok&&r.counters_ok?"yes":"no")<<"\n";rows.push_back(r);}programs.push_back(std::move(pr));}
    write_json(ctx,args,programs,rows,args.out_dir/"vulkan_benchmark_results.json");write_csv(rows,args.out_dir/"vulkan_benchmark_results.csv");bool valid=std::all_of(rows.begin(),rows.end(),[](const BenchRow&r){return r.sample_ok&&r.counters_ok;});for(auto&x:programs)destroy_program(ctx,x.program);vkDestroyPipelineLayout(ctx.device(),layout,nullptr);vkDestroyDescriptorSetLayout(ctx.device(),dsl,nullptr);if(!valid){std::cerr<<"validation failed\n";return 2;}std::cout<<"Wrote native Vulkan benchmark results.\n";return 0;}catch(const std::exception&e){std::cerr<<"UGTS Vulkan benchmark error: "<<e.what()<<"\n";return 1;}}
