package com.spikespaz.radialmenu;

import lombok.SneakyThrows;
import net.minecraft.client.settings.KeyBinding;
import net.minecraftforge.client.settings.KeyConflictContext;
import net.minecraftforge.client.settings.KeyModifier;
import net.minecraftforge.fml.client.registry.ClientRegistry;
import org.lwjgl.input.Keyboard;

import java.lang.reflect.Field;

public class KeyBindings {
    private static final String LANG_PREFIX = "key." + RadialMenu.MOD_ID;
    private static final String CATEGORY = LANG_PREFIX + ".category";

    public static final KeyBinding OPEN_MENU_0 = new KeyBinding(LANG_PREFIX + ".open_menu.0", KeyConflictContext.IN_GAME, Keyboard.KEY_R, CATEGORY);
    public static final KeyBinding EDIT_MENU_0 = new KeyBinding(LANG_PREFIX + ".edit_menu.0", KeyConflictContext.IN_GAME, KeyModifier.ALT, Keyboard.KEY_R, CATEGORY);

    @SneakyThrows
    public static void registerAll() {
        for (Field field : KeyBindings.class.getDeclaredFields()) {
            if (field.getType() != KeyBinding.class)
                continue;

            field.setAccessible(true);
            ClientRegistry.registerKeyBinding((KeyBinding) field.get(null));
        }
    }
}
