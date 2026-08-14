using System;
using UnityEngine;

namespace UGTS
{
    [Serializable]
    public struct TypedState
    {
        public Vector2 position;
        public Vector2 velocity;
        public double time;
        public double phase;
        public int sheet;
        public int orientation;
        public string branch;
        public string lineage;
    }

    [Serializable]
    public struct LinearTrajectory
    {
        public Vector2 p0;
        public Vector2 v0;
        public double t0;

        public Vector2 PositionAt(double t) => p0 + v0 * (float)(t - t0);
    }

    public static class EventSurface
    {
        // Closed-form crossing for n dot (p0 + v*(t-t0)) = offset.
        public static bool NextLineCrossing(
            LinearTrajectory trajectory,
            Vector2 normal,
            double offset,
            double after,
            double before,
            out double eventTime)
        {
            double denominator = Vector2.Dot(normal, trajectory.v0);
            if (Math.Abs(denominator) < 1e-12)
            {
                eventTime = 0.0;
                return false;
            }
            double dt = (offset - Vector2.Dot(normal, trajectory.p0)) / denominator;
            eventTime = trajectory.t0 + dt;
            return eventTime > after && eventTime <= before;
        }
    }

    public class UGTSComponent : MonoBehaviour
    {
        public LinearTrajectory trajectory;
        public int sheet;
        public int orientation = 1;
        public string branch = "A";

        public TypedState StateAt(double t) => new TypedState
        {
            position = trajectory.PositionAt(t),
            velocity = trajectory.v0,
            time = t,
            phase = 0.0,
            sheet = sheet,
            orientation = orientation,
            branch = branch,
            lineage = gameObject.name
        };
    }
}
