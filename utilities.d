import arsd.nanovega: NVGColor, nvgRGBA;
import arsd.color: Color;

public struct PointF {
    float x;
    float y;
}

public struct SizeF {
    float width;
    float height;
}

public NVGColor getNVGColor(Color color) {
    return nvgRGBA(color.r, color.g, color.b, color.a);
}
