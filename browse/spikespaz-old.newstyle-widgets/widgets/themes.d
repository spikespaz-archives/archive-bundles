module widgets.themes;

import arsd.nanovega;
import arsd.color;
import widgets.utilities;

/// Private variable containing the current NanoVega context.
private NVGContext NANOVEGA_CONTEXT;
/// Global variable containing the color of the background widget.
public Color BACKGROUND_COLOR;
/// Global variable containing the active `CheckBoxTheme`.
public CheckBoxTheme CHECK_BOX_THEME;
/// Global variable containing the active `CheckBoxTheme` for the radio button.
public CheckBoxTheme RADIO_BUTTON_THEME;
/// Global variable containing the active `ButtonTheme`.
public ButtonTheme TEXT_BUTTON_THEME;
/// Global variable containing the active `TextLabelTheme`.
public TextLabelTheme TEXT_LABEL_THEME;
/// Global variable containing the active `TextLabelTheme` for button labels.
public TextLabelTheme BUTTON_LABEL_THEME;
/// Global variable containing the active `ScrollBarTheme`.
public ScrollBarTheme SCROLL_BAR_THEME;
/// Global variable containing the `TextLabelTheme` used by text input when the state is default or `ZEROFLAG`.
public TextLabelTheme DEFAULT_TEXT_INPUT_LABEL_THEME;
/// Global variable containing the `TextLabelTheme` used by text input when the state is `HOVERED`.
public TextLabelTheme HOVERED_TEXT_INPUT_LABEL_THEME;
/// Global variable containing the `TextLabelTheme` used by text input when the state is `ACTIVE`.
public TextLabelTheme ACTIVE_TEXT_INPUT_LABEL_THEME;
/// Global variable containing the active `TextInputTheme`.
public TextInputTheme TEXT_INPUT_THEME;
/// Global variable containing the active `ToolTipTheme`.
public ToolTipTheme TOOL_TIP_THEME;

/// Initialize the values of all the global theme variables.
/// This must be called in order for anything to be drawn
/// on the NanoVega canvas, unless you create your own themes.
void initGlobalThemes(NVGContext nvgc) {
    // Private NVGContext.
    NANOVEGA_CONTEXT = nvgc;
    // Public background color default.
    BACKGROUND_COLOR = Color.white();
    // Public check box theme default.
    CHECK_BOX_THEME = CheckBoxTheme(0);
    // Public radio button theme default.
    RADIO_BUTTON_THEME = CheckBoxTheme(0);
    RADIO_BUTTON_THEME.checkImage = NANOVEGA_CONTEXT.createImage("icons/check.png");
    // Public text label theme default.
    TEXT_LABEL_THEME = TextLabelTheme(0);
    // Public text label theme default for labeled text bottons.
    BUTTON_LABEL_THEME = TextLabelTheme(0);
    BUTTON_LABEL_THEME.textSize = 14;
    // Public text button theme default.
    TEXT_BUTTON_THEME = ButtonTheme(0);
    // Public scroll bar theme default.
    SCROLL_BAR_THEME = ScrollBarTheme(0);
    // Public text label theme defaults for the three activity states of text input.
    DEFAULT_TEXT_INPUT_LABEL_THEME = TextLabelTheme(0);
    DEFAULT_TEXT_INPUT_LABEL_THEME.textColor = Color.gray().getNVGColor();
    HOVERED_TEXT_INPUT_LABEL_THEME = TextLabelTheme(0);
    HOVERED_TEXT_INPUT_LABEL_THEME.textColor = Color.gray().getNVGColor();
    ACTIVE_TEXT_INPUT_LABEL_THEME = TextLabelTheme(0);
    ACTIVE_TEXT_INPUT_LABEL_THEME.textColor = Color.black().getNVGColor();
    // Public text input theme default.
    TEXT_INPUT_THEME = TextInputTheme(0);
    /// Public tool tip theme default.
    TOOL_TIP_THEME = ToolTipTheme(0);
}

/// Struct representing the theme for drawable check box widgets.
/// This is also reused for the radio button themes, the only difference is that radius is ignored.
public struct CheckBoxTheme {
    /// The radius of the corners of a checkbox.
    float borderRadius;
    /// The width of the border of a checkbox. Set to 0 to disable.
    float borderWidth;
    /// The image to fill the checkbox with, if state is `CHECKED`.
    NVGImage checkImage;

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
    this(ubyte id, float borderRadius = 2, float borderWidth = 1, NVGImage checkImage = NANOVEGA_CONTEXT.createImage(
            "icons/check.png"), Color uncheckedFillColor = Color.white(), Color checkedFillColor = Color.white(),
            Color hoveredFillColor = Color.gray(), Color activeFillColor = Color.gray(),
            Color uncheckedBorderColor = Color.black(), Color checkedBorderColor = Color.black(),
            Color hoveredBorderColor = Color.black(), Color activeBorderColor = Color.black(),
            Color checkedIconColor = Color.black(), Color hoveredIconColor = Color.black(), Color activeIconColor = Color
            .black()) {
        this.borderRadius = borderRadius;
        this.borderWidth = borderWidth;
        this.checkImage = checkImage;

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

/// Struct representing the theme for scroll bar widgets.
struct ScrollBarTheme {
    /// The radius of the handle.
    float radius;
    /// The width of the scroll bar.
    float width;
    /// The width of the scroll bar border.
    float borderWidth;
    /// The padding between the handle and the track border.
    float borderPadding;

    /// The color of the scroll bar track fill when the state is default or `ZEROFLAG`.
    NVGColor defaultTrackColor;
    /// The color of the scroll bar handle when the state is default or `ZEROFLAG`.
    NVGColor defaultHandleColor;
    /// The color of the scroll bar track outline when the state is default or `ZEROFLAG`.
    NVGColor defaultBorderColor;

    /// The color of the scroll bar track fill when the state is `HOVERED`.
    NVGColor hoveredTrackColor;
    /// The color of the scroll bar handle when the state is `HOVERED`.
    NVGColor hoveredHandleColor;
    /// The color of the scroll bar track outline when the state is `HOVERED`.
    NVGColor hoveredBorderColor;

    /// The color of the scroll bar track fill when the state is `ACTIVE`.
    NVGColor activeTrackColor;
    /// The color of the scroll bar handle when the state is `ACTIVE`.
    NVGColor activeHandleColor;
    /// The color of the scroll bar track outline when the state is `ACTIVE`.
    NVGColor activeBorderColor;

    /// Construct a theme by passing `arsd.color.Color` objects. Parameter `id` is unused, but required.
    this(ubyte id, float radius = 5, float width = 10, float borderWidth = 2, float borderPadding = 2,
            Color defaultTrackColor = Color.white(), Color defaultHandleColor = Color.gray(),
            Color defaultBorderColor = Color.black(), Color hoveredTrackColor = Color.white(),
            Color hoveredHandleColor = Color.black(), Color hoveredBorderColor = Color.black(),
            Color activeTrackColor = Color.white(), Color activeHandleColor = Color.black(), Color activeBorderColor = Color
            .black()) {
        this.radius = radius;
        this.width = width;
        this.borderWidth = borderWidth;
        this.borderPadding = borderPadding;

        this.defaultTrackColor = defaultTrackColor.getNVGColor();
        this.defaultHandleColor = defaultHandleColor.getNVGColor();
        this.defaultBorderColor = defaultBorderColor.getNVGColor();

        this.hoveredTrackColor = hoveredTrackColor.getNVGColor();
        this.hoveredHandleColor = hoveredHandleColor.getNVGColor();
        this.hoveredBorderColor = hoveredBorderColor.getNVGColor();

        this.activeTrackColor = activeTrackColor.getNVGColor();
        this.activeHandleColor = activeHandleColor.getNVGColor();
        this.activeBorderColor = activeBorderColor.getNVGColor();
    }
}

/// Struct representing the theme for drawable text input widgets.
struct TextInputTheme {
    /// The radius of the border corners.
    float borderRadius;
    /// The stroke width of the border.
    float borderWidth;
    /// The padding between the border and the text.
    float borderPadding;

    /// The color of the text when the state is default or `ZEROFLAG`.
    TextLabelTheme defaultTextTheme;
    /// The color of the text when the state is `HOVERED`.
    TextLabelTheme hoveredTextTheme;
    /// The color of the text when the state is `ACTIVE`.
    TextLabelTheme activeTextTheme;

    /// The color of the input box background when the state is default or `ZEROFLAG`.
    NVGColor defaultBackgroundColor;
    /// The color of the input box background when the state is default or `ZEROFLAG`.
    NVGColor defaultBorderColor;

    /// The color of the input box background when the state is `HOVERED`.
    NVGColor hoveredBackgroundColor;
    /// The color of the input box background when the state is `HOVERED`.
    NVGColor hoveredBorderColor;

    /// The color of the input box background when the state is `ACTIVE`.
    NVGColor activeBackgroundColor;
    /// The color of the input box background when the state is `ACTIVE`.
    NVGColor activeBorderColor;

    /// Construct a theme by passing `arsd.color.Color` objects. Parameter `id` is unused, but required.
    this(ubyte id, float borderRadius = 3, float borderWidth = 2, float borderPadding = 4,
            TextLabelTheme defaultTextTheme = DEFAULT_TEXT_INPUT_LABEL_THEME,
            TextLabelTheme hoveredTextTheme = HOVERED_TEXT_INPUT_LABEL_THEME,
            TextLabelTheme activeTextTheme = ACTIVE_TEXT_INPUT_LABEL_THEME,
            Color defaultBackgroundColor = Color.white(),
            Color defaultBorderColor = Color.gray(), Color hoveredBackgroundColor = Color.white(),
            Color hoveredBorderColor = Color.black(), Color activeBackgroundColor = Color.white(), Color activeBorderColor = Color
            .black()) {
        this.borderRadius = borderRadius;
        this.borderWidth = borderWidth;
        this.borderPadding = borderPadding;

        this.defaultTextTheme = defaultTextTheme;
        this.hoveredTextTheme = hoveredTextTheme;
        this.activeTextTheme = activeTextTheme;

        this.defaultBackgroundColor = defaultBackgroundColor.getNVGColor();
        this.defaultBorderColor = defaultBorderColor.getNVGColor();

        this.hoveredBackgroundColor = hoveredBackgroundColor.getNVGColor();
        this.hoveredBorderColor = hoveredBorderColor.getNVGColor();

        this.activeBackgroundColor = activeBackgroundColor.getNVGColor();
        this.activeBorderColor = activeBorderColor.getNVGColor();
    }
}

/// Struct representing the theme for tooltips.
public struct ToolTipTheme {
    /// The distance between the mouse cursor and the tooltip.
    SizeF distance;
    /// The radius of the border of the tooltip.
    float borderRadius;
    /// The width of the border of the tooltip.
    float borderWidth;
    /// The minimum width that the tooltip must occupy.
    float minimumSize;
    /// The maximum width that the tooltip is allowed to occupuy.
    float maximumSize;
    /// The padding on the sides of the text.
    float borderPadding;
    /// The color of the tooltip border.
    NVGColor borderColor;
    /// The color of the tooltip background.
    NVGColor tooltipColor;
    /// The theme of the text inside of the tooltip.
    TextLabelTheme textTheme;

    /// Construct a theme by passing `arsd.color.Color` objects. Parameter `id` is unused, but required.
    this(ubyte id, SizeF distance = SizeF(10, 0), float borderRadius = 3, float borderWidth = 1, float minimumSize = 100, float maximumSize = 250,
            float borderPadding = 4, Color borderColor = Color.black(), Color tooltipColor = Color.white(),
            TextLabelTheme textTheme = TEXT_LABEL_THEME) {
        this.distance = distance;
        this.borderRadius = borderRadius;
        this.borderWidth = borderWidth;
        this.minimumSize = minimumSize;
        this.maximumSize = maximumSize;
        this.borderPadding = borderPadding;
        this.borderColor = borderColor.getNVGColor();
        this.tooltipColor = tooltipColor.getNVGColor();
        this.textTheme = textTheme;
    }
}
