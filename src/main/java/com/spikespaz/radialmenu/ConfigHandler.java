package com.spikespaz.radialmenu;

import lombok.Getter;
import net.minecraftforge.common.config.Config;

@Config(modid = RadialMenu.MOD_ID, name = "RadialMenu")
@Config.LangKey(ConfigHandler.LANG_KEY_PREFIX + ".title")
public class ConfigHandler {
    @Config.Ignore
    public static final String LANG_KEY_PREFIX = "config." + RadialMenu.MOD_ID;

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".circle_radius")
    @Config.Comment("The radius of the inside of the radial menu.")
    public static int circleRadius = 50;

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".dead_zone_radius")
    @Config.Comment("The radius of the dead zone that the mouse must pass to highlight a radial button.")
    public static int deadZoneRadius = 30;

    @Config.LangKey(LANG_KEY_PREFIX + ".label_bg_color")
    @Config.Comment({"Background color of the label in the center of the radial menu.", "ARGB in hexadecimal format (AARRGGBB)."})
    public static String labelBgColor = "CC000000";

    @Config.LangKey(LANG_KEY_PREFIX + ".label_text_color")
    @Config.Comment({"Text color of the label in the center of the radial menu.", "ARGB in hexadecimal format (AARRGGBB)."})
    public static String labelTextColor = "FFFFFFFF";

    @Config.LangKey(LANG_KEY_PREFIX + ".label_text_empty_color")
    @Config.Comment({"Text color of the label in the center of the radial menu when it is empty (button unassigned).", "ARGB in hexadecimal format (AARRGGBB)."})
    public static String labelTextEmptyColor = "FFFF0000";

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".label_padding_x")
    @Config.Comment("Horizontal padding on the left and right of the text for the label in the center of the radial menu.")
    public static int labelPaddingX = 4;

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".label_padding_y")
    @Config.Comment("Vertical padding on the top and bottom of the text for the label in the center of the radial menu.")
    public static int labelPaddingY = 4;

    @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_color")
    @Config.Comment({"Background color of each radial button.", "ARGB in hexadecimal format (AARRGGBB)."})
    public static String buttonBgColor = "CC000000";

    @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_hover_color")
    @Config.Comment({"Background color of each radial button when it is hovered or highlighted.", "ARGB in hexadecimal format (AARRGGBB)."})
    public static String buttonBgHoverColor = "CCFFFFFF";

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".button_thickness")
    @Config.Comment("Thickness or width of each radial button's trapezoid.")
    public static int buttonThickness = 30;

    public static int getLabelBgColor() {
        return (int) Long.parseLong(labelBgColor, 16);
    }

    public static int getLabelTextColor() {
        return (int) Long.parseLong(labelTextColor, 16);
    }

    public static int getLabelTextEmptyColor() {
        return (int) Long.parseLong(labelTextEmptyColor, 16);
    }

    public static int getButtonBgColor() {
        return (int) Long.parseLong(buttonBgColor, 16);
    }

    public static int getButtonBgHoverColor() {
        return (int) Long.parseLong(buttonBgHoverColor, 16);
    }
}
