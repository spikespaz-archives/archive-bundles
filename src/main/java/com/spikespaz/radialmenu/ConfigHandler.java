package com.spikespaz.radialmenu;

import lombok.Getter;
import net.minecraftforge.common.config.Config;

@Config(modid = RadialMenu.MOD_ID, name = "RadialMenu")
public class ConfigHandler {
    @Getter
    @Config.Name("Inner Circle Radius")
    @Config.Comment("The radius of the inside of the radial menu.")
    private static int circleRadius = 50;

    @Getter
    @Config.Name("Dead Zone Radius")
    @Config.Comment("The radius of the dead zone that the mouse must pass to highlight a radial button.")
    private static int deadZoneRadius = 30;

    @Config.Name("Label Background Color")
    @Config.Comment({"Background color of the label in the center of the radial menu.", "ARGB in hexadecimal format (AARRGGBB)."})
    private static String labelBgColor = "CC000000";

    @Config.Name("Label Text Color")
    @Config.Comment({"Text color of the label in the center of the radial menu.", "ARGB in hexadecimal format (AARRGGBB)."})
    private static String labelTextColor = "FFFFFFFF";

    @Getter
    @Config.Name("Horizontal Label Padding")
    @Config.Comment("Horizontal padding on the left and right of the text for the label in the center of the radial menu.")
    private static int labelPaddingX = 4;

    @Getter
    @Config.Name("Vertical Label Padding")
    @Config.Comment("Vertical padding on the top and bottom of the text for the label in the center of the radial menu.")
    private static int labelPaddingY = 4;

    @Config.Name("Button Background Color")
    @Config.Comment({"Background color of each radial button.", "ARGB in hexadecimal format (AARRGGBB)."})
    private static String buttonBgColor = "CC000000";

    @Config.Name("Hovered Button Background Color")
    @Config.Comment({"Background color of each radial button when it is hovered or highlighted.", "ARGB in hexadecimal format (AARRGGBB)."})
    private static String buttonBgHoverColor = "CCFFFFFF";

    @Getter
    @Config.Name("Button Thickness")
    @Config.Comment("Thickness or width of each radial button's trapezoid.")
    private static int buttonThickness = 30;

    public static int getLabelBgColor() {
        return (int) Long.parseLong(labelBgColor, 16);
    }

    public static int getLabelTextColor() {
        return (int) Long.parseLong(labelTextColor, 16);
    }

    public static int getButtonBgColor() {
        return (int) Long.parseLong(buttonBgColor, 16);
    }

    public static int getButtonBgHoverColor() {
        return (int) Long.parseLong(buttonBgHoverColor, 16);
    }
}
