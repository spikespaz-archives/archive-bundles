package com.spikespaz.radialmenu;

import lombok.SneakyThrows;
import net.minecraft.client.settings.KeyBinding;
import net.minecraftforge.fml.common.FMLCommonHandler;

import java.lang.reflect.Field;

public class Utilities {
    public interface ICallback<T> {
        void resolve(T param);
    }

    @SneakyThrows
    public static void emitKeyEvent(KeyBinding binding) {
        final Field field = KeyBinding.class.getDeclaredField("pressTime");

        field.setAccessible(true);
        field.set(binding, 1);

        FMLCommonHandler.instance().fireKeyInput();
    }
}
