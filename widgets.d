import arsd.nanovega;
import arsd.color;
public import themes;
public import utilities;

public enum : ubyte {
    UNCHECKED = 0,
    CHECKED = 1,
    HOVERED = 2,
    ACTIVE = 4
}

public void drawCheckBox(NVGContext nvgc, PointF pos, SizeF size = SizeF(14f, 14f), ubyte flags = 0) {
    nvgc.beginPath();

    final switch (flags) {
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
