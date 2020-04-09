package com.spikespaz.radialmenu;

import lombok.Getter;
import net.minecraft.init.SoundEvents;
import net.minecraft.util.SoundEvent;
import net.minecraftforge.common.config.Config;

@Config(modid = RadialMenu.MOD_ID, name = "RadialMenu")
@Config.LangKey(ConfigHandler.LANG_KEY_PREFIX + ".title")
public class ConfigHandler {
    @Config.Ignore
    public static final String LANG_KEY_PREFIX = "config." + RadialMenu.MOD_ID;

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".circle_radius")
    @Config.Comment("The radius of the inside of the radial menu.")
    @Config.RangeInt(min = 0)
    public static int circleRadius = 70;

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".dead_zone_radius")
    @Config.Comment("The radius of the dead zone that the mouse must pass to highlight a radial button.")
    @Config.RangeInt(min = 0)
    public static int deadZoneRadius = 30;

    @Config.LangKey(LANG_KEY_PREFIX + ".label_bg_color")
    @Config.Comment({"Background color of the label in the center of the radial menu.", "RGB in hexadecimal format (RRGGBB)."})
    public static String labelBgColor = "000000";

    @Config.LangKey(LANG_KEY_PREFIX + ".label_bg_opacity")
    @Config.Comment("Background opacity of the label in the center of the radial menu.")
    @Config.RangeDouble(min = 0, max = 1)
    public static double labelBgOpacity = 0.75;

    @Config.LangKey(LANG_KEY_PREFIX + ".label_text_color")
    @Config.Comment({"Text color of the label in the center of the radial menu.", "RGB in hexadecimal format (RRGGBB)."})
    public static String labelTextColor = "FFFFFF";

    @Config.LangKey(LANG_KEY_PREFIX + ".label_text_opacity")
    @Config.Comment("Text opacity of the label in the center of the radial menu.")
    @Config.RangeDouble(min = 0, max = 1)
    public static double labelTextOpacity = 1.0;

    @Config.LangKey(LANG_KEY_PREFIX + ".label_text_empty_color")
    @Config.Comment({"Text color of the label in the center of the radial menu when it is empty (button unassigned).", "RGB in hexadecimal format (RRGGBB)."})
    public static String labelTextEmptyColor = "FE3F3F";

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".label_padding_x")
    @Config.Comment("Horizontal padding on the left and right of the text for the label in the center of the radial menu.")
    @Config.RangeInt(min = 0)
    public static int labelPaddingX = 4;

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".label_padding_y")
    @Config.Comment("Vertical padding on the top and bottom of the text for the label in the center of the radial menu.")
    @Config.RangeInt(min = 0)
    public static int labelPaddingY = 4;

    @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_color")
    @Config.Comment({"Background color of each radial button.", "RGB in hexadecimal format (RRGGBB)."})
    public static String buttonBgColor = "000000";

    @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_opacity")
    @Config.Comment("Background opacity of each radial button.")
    @Config.RangeDouble(min = 0, max = 1)
    public static double buttonBgOpacity = 0.75;

    @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_hover_color")
    @Config.Comment({"Background color of each radial button when it is hovered or highlighted.", "RGB in hexadecimal format (RRGGBB)."})
    public static String buttonBgHoverColor = "CC0000";

    @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_hover_opacity")
    @Config.Comment("Background opacity of each radial button when it is hovered or highlighted.")
    @Config.RangeDouble(min = 0, max = 1)
    public static double buttonBgHoverOpacity = 1.0;

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".button_thickness")
    @Config.Comment("Thickness or width of each radial button's trapezoid.")
    @Config.RangeInt(min = 0)
    public static int buttonThickness = 30;

    @Config.LangKey(LANG_KEY_PREFIX + ".button_sound_event")
    @Config.Comment("The sound for a radial button when it is pressed.")
    public static String buttonSoundEvent = "UI_BUTTON_CLICK";

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".button_sound_pitch")
    @Config.Comment("The pitch of the sound for a radial button when it is pressed.")
    @Config.RangeDouble(min = 0.5, max = 2.0)
    public static double buttonSoundPitch = 2.0;

    @Getter
    @Config.LangKey(LANG_KEY_PREFIX + ".button_sound_enabled")
    @Config.Comment("Enable button press sound for radial button.")
    public static boolean buttonSoundEnabled = true;

    public static int getLabelBgColor() {
        return (int) (labelBgOpacity * 0xFF) << 24 | (int) Long.parseLong(labelBgColor, 16);
    }

    public static int getLabelTextColor() {
        return (int) (labelTextOpacity * 0xFF) << 24 | (int) Long.parseLong(labelTextColor, 16);
    }

    public static int getLabelTextEmptyColor() {
        return (int) (labelTextOpacity * 0xFF) << 24 | (int) Long.parseLong(labelTextEmptyColor, 16);
    }

    public static int getButtonBgColor() {
        return (int) (buttonBgOpacity * 0xFF) << 24 | (int) Long.parseLong(buttonBgColor, 16);
    }

    public static int getButtonBgHoverColor() {
        return (int) (buttonBgHoverOpacity * 0xFF) << 24 | (int) Long.parseLong(buttonBgHoverColor, 16);
    }

    public static SoundEvent getButtonSoundEvent() {
        try {
            SoundEvents.class.getDeclaredField(buttonSoundEvent);
            return (SoundEvent) SoundEvents.class.getDeclaredField(buttonSoundEvent).get(null);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            e.printStackTrace();
            return SoundEvents.ENTITY_CHICKEN_EGG;
        }
    }
}
