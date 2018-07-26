import arsd.nanovega: NVGColor;
import arsd.color;
import utilities;

public CheckBoxTheme CHECK_BOX_THEME = CheckBoxTheme(0);

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
