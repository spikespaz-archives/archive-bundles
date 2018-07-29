module utilities;

import arsd.nanovega: NVGColor, nvgRGBA;
import arsd.color: Color;

public enum : ushort {
    /// Blank flag for no state.
    ZEROFLAG = 0,
    /// Draw a checkable widget as if it were unchecked. (default)
    UNCHECKED = 1,
    /// Draw a checkable widget as if it were checked.
    CHECKED = 2,
    /// Draw a widget as if the mouse was hovered over it.
    HOVERED = 4,
    /// Draw a widget as if it was actively selected or being clicked.
    ACTIVE = 8,
    /// Center elements vertically. (default)
    CENTER_VERTICAL = 16,
    /// Center elements horizontally.
    CENTER_HORIZONTAL = 32,
    /// Align child elements to left of bounding box. (default)
    ALIGN_LEFT = 64,
    /// Align child elements to right of bounding box.
    ALIGN_RIGHT = 128,
    /// Align child elements to top of bounding box.
    ALIGN_TOP = 256,
    /// Align child elements to bottom of bounding box.
    ALIGN_BOTTOM = 512
}

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

/// Compare a bitfield and check if a flag is present.
public bool checkFlag(const ushort field, const ushort flag) {
    return ((field & flag) == flag);
}
