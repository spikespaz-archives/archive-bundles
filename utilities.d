import arsd.nanovega: NVGColor, nvgRGBA;
import arsd.color: Color;

/// A tuple-like struct representing 2D float coordinates in space.
public struct PointF {
    /// Arbitrary floating point unit representing an X-coordinate of a point in space.
    float x;
    /// Arbitrary floating point unit representing an Y-coordinate of a point in space.
    float y;
}

/// A tuple-like struct, similar to PointF, but for the size of widgets.
public struct SizeF {
    /// Arbitrary floating point unit representing the width of a widget.
    float width;
    /// Arbitrary floating point unit representing the height of a widget.
    float height;
}

/// A utility function to convert a `arsd.color.Color` object to `arsd.nanovega.NVGColor`.
public NVGColor getNVGColor(Color color) {
    return nvgRGBA(color.r, color.g, color.b, color.a);
}
