package com.spikespaz.radialmenu;

import lombok.Getter;
import net.minecraft.init.SoundEvents;
import net.minecraft.util.SoundEvent;
import net.minecraftforge.common.config.Config;

@Config(modid = RadialMenu.MOD_ID, name = "RadialMenu")
public final class ConfigHandler {
    @Config.Ignore
    public static final String LANG_KEY_PREFIX = "config." + RadialMenu.MOD_ID;

    @Config.LangKey(LANG_KEY_PREFIX + ".category.general")
    public static final GeneralOptions GENERAL = GeneralOptions.INSTANCE;
    @Config.LangKey(LANG_KEY_PREFIX + ".category.label")
    public static final LabelOptions LABEL = LabelOptions.INSTANCE;
    @Config.LangKey(LANG_KEY_PREFIX + ".category.button")
    public static final ButtonOptions BUTTON = ButtonOptions.INSTANCE;
    @Config.LangKey(LANG_KEY_PREFIX + ".category.sound")
    public static final SoundOptions SOUND = SoundOptions.INSTANCE;

    public static final class GeneralOptions {
        @Config.Ignore
        public static final GeneralOptions INSTANCE = new GeneralOptions();

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".circle_radius")
        @Config.Comment("The radius of the inside of the radial menu.")
        @Config.RangeInt(min = 0)
        public int circleRadius = 70;

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".dead_zone_radius")
        @Config.Comment("The radius of the dead zone that the mouse must pass to highlight a radial button.")
        @Config.RangeInt(min = 0)
        public int deadZoneRadius = 30;
    }

    public static final class LabelOptions {
        @Config.Ignore
        public static final LabelOptions INSTANCE = new LabelOptions();

        @Config.LangKey(LANG_KEY_PREFIX + ".label_bg_color")
        @Config.Comment({"Background color of the label in the center of the radial menu.", "RGB in hexadecimal format (RRGGBB)."})
        public String labelBgColor = "000000";

        @Config.LangKey(LANG_KEY_PREFIX + ".label_bg_opacity")
        @Config.Comment("Background opacity of the label in the center of the radial menu.")
        @Config.RangeDouble(min = 0, max = 1)
        public double labelBgOpacity = 0.75;

        @Config.LangKey(LANG_KEY_PREFIX + ".label_text_color")
        @Config.Comment({"Text color of the label in the center of the radial menu.", "RGB in hexadecimal format (RRGGBB)."})
        public String labelTextColor = "FFFFFF";

        @Config.LangKey(LANG_KEY_PREFIX + ".label_text_opacity")
        @Config.Comment("Text opacity of the label in the center of the radial menu.")
        @Config.RangeDouble(min = 0, max = 1)
        public double labelTextOpacity = 1.0;

        @Config.LangKey(LANG_KEY_PREFIX + ".label_text_empty_color")
        @Config.Comment({"Text color of the label in the center of the radial menu when it is empty (button unassigned).", "RGB in hexadecimal format (RRGGBB)."})
        public String labelTextEmptyColor = "FE3F3F";

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".label_padding_x")
        @Config.Comment("Horizontal padding on the left and right of the text for the label in the center of the radial menu.")
        @Config.RangeInt(min = 0)
        public int labelPaddingX = 4;

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".label_padding_y")
        @Config.Comment("Vertical padding on the top and bottom of the text for the label in the center of the radial menu.")
        @Config.RangeInt(min = 0)
        public int labelPaddingY = 4;

        public int getLabelBgColor() {
            return (int) (this.labelBgOpacity * 0xFF) << 24 | (int) Long.parseLong(this.labelBgColor, 16);
        }

        public int getLabelTextColor() {
            return (int) (this.labelTextOpacity * 0xFF) << 24 | (int) Long.parseLong(this.labelTextColor, 16);
        }

        public int getLabelTextEmptyColor() {
            return (int) (this.labelTextOpacity * 0xFF) << 24 | (int) Long.parseLong(this.labelTextEmptyColor, 16);
        }
    }

    public static final class ButtonOptions {
        @Config.Ignore
        public static final ButtonOptions INSTANCE = new ButtonOptions();

        @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_color")
        @Config.Comment({"Background color of each radial button.", "RGB in hexadecimal format (RRGGBB)."})
        public String buttonBgColor = "000000";

        @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_opacity")
        @Config.Comment("Background opacity of each radial button.")
        @Config.RangeDouble(min = 0, max = 1)
        public double buttonBgOpacity = 0.75;

        @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_hover_color")
        @Config.Comment({"Background color of each radial button when it is hovered or highlighted.", "RGB in hexadecimal format (RRGGBB)."})
        public String buttonBgHoverColor = "CC0000";

        @Config.LangKey(LANG_KEY_PREFIX + ".button_bg_hover_opacity")
        @Config.Comment("Background opacity of each radial button when it is hovered or highlighted.")
        @Config.RangeDouble(min = 0, max = 1)
        public double buttonBgHoverOpacity = 1.0;

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".button_icon_opacity")
        @Config.Comment("Opacity of each radial button icon.")
        @Config.RangeDouble(min = 0, max = 1)
        public double buttonIconOpacity = 1.0;

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".button_icon_hover_opacity")
        @Config.Comment("Opacity of each radial button icon when it is hovered or highlighted.")
        @Config.RangeDouble(min = 0, max = 1)
        public double buttonIconHoverOpacity = 1.0;

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".button_thickness")
        @Config.Comment("Thickness or width of each radial button's trapezoid.")
        @Config.RangeInt(min = 0)
        public int buttonThickness = 30;

        public int getButtonBgColor() {
            return (int) (this.buttonBgOpacity * 0xFF) << 24 | (int) Long.parseLong(this.buttonBgColor, 16);
        }

        public int getButtonBgHoverColor() {
            return (int) (this.buttonBgHoverOpacity * 0xFF) << 24 | (int) Long.parseLong(this.buttonBgHoverColor, 16);
        }
    }

    public static final class SoundOptions {
        @Config.Ignore
        public static final SoundOptions INSTANCE = new SoundOptions();

        @Config.LangKey(LANG_KEY_PREFIX + ".button_sound_event")
        @Config.Comment("The sound for a radial button when it is pressed.")
        public String buttonSoundEvent = "UI_BUTTON_CLICK";

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".button_sound_pitch")
        @Config.Comment("The pitch of the sound for a radial button when it is pressed.")
        @Config.RangeDouble(min = 0.5, max = 2.0)
        public double buttonSoundPitch = 2.0;

        @Getter
        @Config.LangKey(LANG_KEY_PREFIX + ".button_sound_enabled")
        @Config.Comment("Enable button press sound for radial button.")
        public boolean buttonSoundEnabled = true;

        public SoundEvent getButtonSoundEvent() {
            try {
                SoundEvents.class.getDeclaredField(this.buttonSoundEvent);
                return (SoundEvent) SoundEvents.class.getDeclaredField(this.buttonSoundEvent).get(null);
            } catch (NoSuchFieldException | IllegalAccessException e) {
                e.printStackTrace();
                return SoundEvents.ENTITY_CHICKEN_EGG;
            }
        }
    }
}
