package com.spikespaz.radialmenu;

public class MathHelper {
    public static final double TWO_PI = Math.PI * 2;

    public static double normAngle(double angle) {
        return normAngle(angle, TWO_PI);
    }

    public static double normAngle(double angle, double range) {
        return (angle % range + range) % range;
    }

    public static double angleDiff(double a0, double a1) {
        double r = (a0 - a1) % TWO_PI;
        if (r < -Math.PI)
            r += TWO_PI;
        if (r >= Math.PI)
            r -= TWO_PI;
        return r;
    }

    public static boolean isAngleBetween(double start, double end, double mid) {
        start = normAngle(start);
        end = normAngle(normAngle(end) - start);
        mid = normAngle(normAngle(mid) - start);
        return (mid < end);
    }
}
