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
        final Field field = KeyBinding.class.getDeclaredField("pressTime");

        field.setAccessible(true);
        field.set(binding, 1);

        FMLCommonHandler.instance().fireKeyInput();
    }

    public static KeyBinding getKeyBindByName(String name) {
        for (KeyBinding binding : mc.gameSettings.keyBindings)
            if (binding.getKeyDescription().equals(name))
                return binding;

        return null;
    }
}
