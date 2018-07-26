import arsd.nanovega;
import arsd.color;
public import utilities;

public enum : ubyte {
    UNCHECKED = 0,
    CHECKED = 1,
    HOVERED = 2,
    ACTIVE = 4
}

public struct CheckBoxTheme {
    float borderRadius;
    float borderWidth;

    NVGColor uncheckedFillColor;
    NVGColor checkedFillColor;
    NVGColor hoveredFillColor;
    NVGColor activeFillColor;

    NVGColor uncheckedBorderColor;
    NVGColor checkedBorderColor;
    NVGColor hoveredBorderColor;
    NVGColor activeBorderColor;

    NVGColor checkedIconColor;
    NVGColor hoveredIconColor;
    NVGColor activeIconColor;

    this(ubyte id, float borderRadius = 0, float borderWidth = 1, Color uncheckedFillColor = Color.white(),
            Color checkedFillColor = Color.white(), Color hoveredFillColor = Color.gray(),
            Color activeFillColor = Color.gray(), Color uncheckedBorderColor = Color.black(),
            Color checkedBorderColor = Color.black(), Color hoveredBorderColor = Color.black(),
            Color activeBorderColor = Color.black(), Color checkedIconColor = Color.black(),
            Color hoveredIconColor = Color.black(), Color activeIconColor = Color.black()) {
        this.borderRadius = borderRadius;
        this.borderWidth = borderWidth;

        this.uncheckedFillColor = uncheckedFillColor.getNVGColor();
        this.checkedFillColor = checkedFillColor.getNVGColor();
        this.hoveredFillColor = hoveredFillColor.getNVGColor();
        this.activeFillColor = activeFillColor.getNVGColor();

        this.uncheckedBorderColor = uncheckedBorderColor.getNVGColor();
        this.checkedBorderColor = checkedBorderColor.getNVGColor();
        this.hoveredBorderColor = hoveredBorderColor.getNVGColor();
        this.activeBorderColor = activeBorderColor.getNVGColor();

        this.checkedIconColor = checkedIconColor.getNVGColor();
        this.hoveredIconColor = hoveredIconColor.getNVGColor();
        this.activeIconColor = activeIconColor.getNVGColor();
    }
}

public CheckBoxTheme CHECK_BOX_THEME = CheckBoxTheme(0);

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
