package com.spikespaz.radialmenu;

import lombok.SneakyThrows;
import net.minecraft.client.Minecraft;
import net.minecraft.client.settings.KeyBinding;
import net.minecraftforge.fml.common.FMLCommonHandler;

import java.lang.reflect.Field;

public final class Utilities {
    private static Minecraft mc = Minecraft.getMinecraft();

    public interface ICallback<T> {
        void resolve(T param);
    }

    @SneakyThrows
    public static void emitKeyBindEvent(KeyBinding binding) {
        final Field pressTime = KeyBinding.class.getDeclaredField("pressTime");
        final Field pressed = KeyBinding.class.getDeclaredField("pressed");

        pressTime.setAccessible(true);
        pressed.setAccessible(true);

        pressTime.set(binding, 1);
        pressed.set(binding, true);

        FMLCommonHandler.instance().fireKeyInput();

        pressTime.set(binding, 0);
        pressed.set(binding, false);
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
}
