import arsd.nanovega: NVGColor;
import arsd.color;
import utilities;
import std.stdio: writeln;

/// Global variable containing the color of the background widget.
public Color BACKGROUND_COLOR;
/// Global variable containing the active `CheckBoxTheme`.
public CheckBoxTheme CHECK_BOX_THEME;
/// Global variable containing the active `ButtonTheme`.
public ButtonTheme TEXT_BUTTON_THEME;
/// Global variable containing the active `TextLabelTheme`.
public TextLabelTheme TEXT_LABEL_THEME;
/// Global variable containing the active `TextLabelTheme` for button labels.
public TextLabelTheme BUTTON_LABEL_THEME;

/// Initialize the values of all the global theme variables.
/// This must be called in order for anything to be drawn
/// on the NanoVega canvas, unless you create your own themes.
void initGlobalThemes() {
    BACKGROUND_COLOR = Color.white();
    CHECK_BOX_THEME = CheckBoxTheme(0);
    TEXT_LABEL_THEME = TextLabelTheme(0);
    BUTTON_LABEL_THEME = TextLabelTheme(0);
    BUTTON_LABEL_THEME.textSize = 14;
    TEXT_BUTTON_THEME = ButtonTheme(0);
}

/// Struct representing the theme for drawable check box widgets.
public struct CheckBoxTheme {
    /// The radius of the corners of a checkbox.
    float borderRadius;
    /// The width of the border of a checkbox. Set to 0 to disable.
    float borderWidth;

    /// The fill color of a checkbox when the state is `UNCHECKED` or `ZEROFLAG`.
    NVGColor uncheckedFillColor;
    /// The fill color of a checkbox when the state is `CHECKED`.
    NVGColor checkedFillColor;
    /// The fill color of a checkbox when the state is `HOVERED`.
    NVGColor hoveredFillColor;
    /// The fill color of a checkbox when the state is `ACTIVE`.
    NVGColor activeFillColor;

    /// The outline or border color of a checkbox when the state is `UNCHECKED` or `ZEROFLAG`.
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
    this(ubyte id, float borderRadius = 2, float borderWidth = 1, Color uncheckedFillColor = Color.white(),
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

/// Struct representing the theme for drawable check box widgets.
public struct ButtonTheme {
    /// The radius of the corners of a button.
    float borderRadius;
    /// The width of the border of a button. Set to 0 to disable.
    float borderWidth;
    /// The padding on every side of the text.
    float textPadding;

    /// The fill color of a button when the state is default or `ZEROFLAG`.
    NVGColor defaultFillColor;
    /// The fill color of a button when the state is `HOVERED`.
    NVGColor hoveredFillColor;
    /// The fill color of a button when the state is `ACTIVE`.
    NVGColor activeFillColor;

    /// The theme for the label when the state is default or `ZEROFLAG`.
    TextLabelTheme defaultTextTheme;
    /// The theme for the label when the state is `HOVERED`.
    TextLabelTheme hoveredTextTheme;
    /// The theme for the label when the state is `ACTIVE`.
    TextLabelTheme activeTextTheme;

    /// The outline or border color of a button when the state is default or `ZEROFLAG`.
    NVGColor defaultBorderColor;
    /// The outline or border color of a button when the state is `HOVERED`.
    NVGColor hoveredBorderColor;
    /// The outline or border color of a button when the state is `ACTIVE`.
    NVGColor activeBorderColor;

    /// Construct a theme by passing `arsd.color.Color` objects. Parameter `id` is unused, but required.
    this(ubyte id, float borderRadius = 2, float borderWidth = 1, float textPadding = 4,
            Color defaultFillColor = Color.white(), Color hoveredFillColor = Color.gray(),
            Color activeFillColor = Color.gray(),
            TextLabelTheme defaultTextTheme = BUTTON_LABEL_THEME,
            TextLabelTheme hoveredTextTheme = BUTTON_LABEL_THEME,
            TextLabelTheme activeTextTheme = BUTTON_LABEL_THEME, Color defaultBorderColor = Color.black(),
            Color hoveredBorderColor = Color.black(), Color activeBorderColor = Color.black()) {
        this.borderRadius = borderRadius;
        this.borderWidth = borderWidth;
        this.textPadding = textPadding;

        this.defaultFillColor = defaultFillColor.getNVGColor();
        this.hoveredFillColor = hoveredFillColor.getNVGColor();
        this.activeFillColor = hoveredFillColor.getNVGColor();

        this.defaultTextTheme = activeTextTheme;
        this.hoveredTextTheme = activeTextTheme;
        this.activeTextTheme = activeTextTheme;

        this.defaultBorderColor = defaultBorderColor.getNVGColor();
        this.hoveredBorderColor = hoveredBorderColor.getNVGColor();
        this.activeBorderColor = activeBorderColor.getNVGColor();
    }
}

/// Struct representing the theme for drawable text label widgets.
struct TextLabelTheme {
    /// The size of the text.
    float textSize;
    /// The intensity of the blur effect.
    float textBlur;
    /// The spacing between characters.
    float textSpacing;
    /// The string representing the font, will be searched for in 'fonts/' if not registered.
    string textFont;
    /// The color of the text.
    NVGColor textColor;

    /// Construct a theme by passing `arsd.color.Color` objects. Parameter `id` is unused, but required.
    this(ubyte id, float textSize = 16, float textBlur = 0, float textSpacing = 0, string textFont = "Arial", Color textColor = Color
            .black()) {
        this.textSize = textSize;
        this.textBlur = textBlur;
        this.textSpacing = textSpacing;
        this.textFont = textFont;
        this.textColor = textColor.getNVGColor();
    }
}
