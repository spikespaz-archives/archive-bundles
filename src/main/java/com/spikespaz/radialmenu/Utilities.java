package com.spikespaz.radialmenu;

import net.minecraft.client.Minecraft;
import net.minecraft.client.settings.KeyBinding;
import net.minecraftforge.fml.common.FMLCommonHandler;

import java.util.ArrayList;
import java.util.List;

public final class Utilities {
    private static final Minecraft mc = Minecraft.getMinecraft();
    private static final List<KeyBinding> firedKeyBinds = new ArrayList<>();
    private static final List<KeyBinding> toggledKeyBinds = new ArrayList<>();

    public interface ICallback<T> {
        void resolve(T param);
    }

    private static void fireKeyInputEvent() {
        final boolean oldFocus = mc.inGameHasFocus;
        mc.inGameHasFocus = true;
        FMLCommonHandler.instance().fireKeyInput();
        mc.inGameHasFocus = oldFocus;
    }

    public static void fireKey(KeyBinding binding) {
        firedKeyBinds.add(binding);
        binding.pressTime = 1;
        binding.pressed = true;

        fireKeyInputEvent();
    }

    public static void toggleKey(KeyBinding binding) {
        if (!toggledKeyBinds.contains(binding)) {
            toggledKeyBinds.add(binding);
            binding.pressTime = 1;
            binding.pressed = true;
        } else
            binding.pressed = false;

        fireKeyInputEvent();
    }

    public static KeyBinding getKeyBindByName(String name) {
        for (KeyBinding binding : mc.gameSettings.keyBindings)
            if (binding.getKeyDescription().equals(name))
                return binding;

        return null;
    }

    public static void focusGame() {
        mc.displayGuiScreen(null);

        if (mc.currentScreen == null)
            mc.setIngameFocus();
    }

    public static int[] intToRgb(int color) {
        return new int[]{color >> 16 & 255, color >> 8 & 255, color & 255};
    }

    public static int rgbToInt(int red, int green, int blue) {
        return red << 16 | green << 8 | blue;
    }

    public static int interpolateValue(int fromValue, int toValue, double factor) {
        return (int) (fromValue + (toValue - fromValue) * factor);
    }

    public static int interpolateColor(int fromColor, int toColor, double factor) {
        final int[] fromRgb = intToRgb(fromColor);
        final int[] toRgb = intToRgb(toColor);
        final int[] interRgb = new int[]{
                interpolateValue(fromRgb[0], toRgb[0], factor),
                interpolateValue(fromRgb[1], toRgb[1], factor),
                interpolateValue(fromRgb[2], toRgb[2], factor),
        };

        return rgbToInt(interRgb[0], interRgb[1], interRgb[2]);
    }
}
