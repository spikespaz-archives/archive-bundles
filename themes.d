import arsd.nanovega: NVGColor;
import arsd.color;
import utilities;

/// Global variable containing the active `CheckBoxTheme`.
public CheckBoxTheme CHECK_BOX_THEME = CheckBoxTheme(0);

/// Struct representing the theme for drawable check box widgets.
public struct CheckBoxTheme {
    /// The radius of the corners of a checkbox.
    float borderRadius;
    /// The width of the border of a checkbox. Set to 0 to disable.
    float borderWidth;

    /// The fill color of a checkbox when the state is `UNCHECKED`.
    NVGColor uncheckedFillColor;
    /// The fill color of a checkbox when the state is `CHECKED`.
    NVGColor checkedFillColor;
    /// The fill color of a checkbox when the state is `HOVERED`.
    NVGColor hoveredFillColor;
    /// The fill color of a checkbox when the state is `ACTIVE`.
    NVGColor activeFillColor;

    /// The outline or border color of a checkbox when the state is `UNCHECKED`.
    NVGColor uncheckedBorderColor;
    /// The outline or border color of a checkbox when the state is `CHECKED`.
    NVGColor checkedBorderColor;
    /// The outline or border color of a checkbox when the state is `HOVERED`.
    NVGColor hoveredBorderColor;
    /// The outline or border color of a checkbox when the state is `ACTIVE`.
    NVGColor activeBorderColor;

    /// The color of the check icon of a checkbox when the state is `CHECKED`.
    NVGColor checkedIconColor;
    /// The color of the check icon of a checkbox when the state is `HOVERED`.
    NVGColor hoveredIconColor;
    /// The color of the check icon of a checkbox when the state is `ACTIVE`.
    NVGColor activeIconColor;

    /// Construct a theme by passing `arsd.color.Color` objects. Parameter `id` is unused, but required.
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
