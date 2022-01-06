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
        return (normAngle(normAngle(mid) - start) < normAngle(normAngle(end) - start));
    }

    public static double[] centroid(double[][] vertices) {
        double sumX = 0;
        double sumY = 0;

        for (double[] vertex : vertices) {
            sumX += vertex[0];
            sumY += vertex[1];
        }

        return new double[]{sumX / vertices.length, sumY / vertices.length};
    }
}
