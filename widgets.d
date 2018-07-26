import arsd.nanovega;
import arsd.color;
public import themes;
public import utilities;

public enum : ubyte {
    /// Draw a checkable widget as if it were unchecked. (default)
    UNCHECKED = 0,
    /// Draw a checkable widget as if it were checked.
    CHECKED = 1,
    /// Draw a widget as if the mouse was hovered over it.
    HOVERED = 2,
    /// Draw a widget as if it was actively selected or being clicked.
    ACTIVE = 4
}

/// Draw a simple rectangle the color of `BACKGROUND_COLOR` on the NanoVega context.
public void drawBackground(NVGContext nvgc, PointF pos, SizeF size) {
    nvgc.beginPath();
    nvgc.fillColor = BACKGROUND_COLOR.getNVGColor();
    nvgc.rect(pos.x, pos.y, size.width, size.height);
    nvgc.fill();
}

/// Draw a check box to a NanoVega context, according to the active theme at `CHECK_BOX_THEME`.
public void drawCheckBox(NVGContext nvgc, PointF pos, SizeF size = SizeF(14f, 14f), ubyte state = 0) {
    nvgc.beginPath();

    final switch (state) {
    case ACTIVE:
        nvgc.fillColor = CHECK_BOX_THEME.activeFillColor;
        nvgc.strokeColor = CHECK_BOX_THEME.activeBorderColor;
        break;
    case HOVERED:
        nvgc.fillColor = CHECK_BOX_THEME.hoveredFillColor;
        nvgc.strokeColor = CHECK_BOX_THEME.hoveredBorderColor;
        break;
    case CHECKED:
        nvgc.fillColor = CHECK_BOX_THEME.checkedFillColor;
        nvgc.strokeColor = CHECK_BOX_THEME.checkedBorderColor;
        break;
    case UNCHECKED:
        nvgc.fillColor = CHECK_BOX_THEME.uncheckedFillColor;
        nvgc.strokeColor = CHECK_BOX_THEME.uncheckedBorderColor;
    }

    nvgc.strokeWidth = CHECK_BOX_THEME.borderWidth;

    if (!CHECK_BOX_THEME.borderRadius)
        nvgc.rect(pos.x, pos.y, size.width, size.height);
    else
        nvgc.roundedRect(pos.x, pos.y, size.width, size.height, CHECK_BOX_THEME.borderRadius);

    nvgc.fill();
    nvgc.stroke();
}
