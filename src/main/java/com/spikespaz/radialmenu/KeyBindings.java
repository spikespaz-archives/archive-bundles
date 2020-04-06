package com.spikespaz.radialmenu;

import lombok.SneakyThrows;
import net.minecraft.client.settings.KeyBinding;
import net.minecraftforge.client.settings.KeyConflictContext;
import net.minecraftforge.fml.client.registry.ClientRegistry;
import org.lwjgl.input.Keyboard;

import java.lang.reflect.Field;

public class KeyBindings {
    private static final String LANG_PREFIX = "key." + RadialMenu.MOD_ID;

    private static final String CATEGORY = LANG_PREFIX + ".category";

    public static KeyBinding openMenu0;

    public static void initialize() {
        openMenu0 = new KeyBinding(LANG_PREFIX + ".open_menu.0", KeyConflictContext.IN_GAME, Keyboard.KEY_X, CATEGORY);
    }

    @SneakyThrows
    public static void register() {
        for (Field field : KeyBindings.class.getDeclaredFields()) {
            if (field.getType() != KeyBinding.class)
                continue;

            field.setAccessible(true);
            ClientRegistry.registerKeyBinding((KeyBinding) field.get(null));
        }
    }
}
