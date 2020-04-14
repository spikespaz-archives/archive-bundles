package com.spikespaz.radialmenu;

import lombok.SneakyThrows;
import net.minecraft.client.settings.KeyBinding;
import net.minecraftforge.client.settings.KeyConflictContext;
import net.minecraftforge.client.settings.KeyModifier;
import net.minecraftforge.fml.client.registry.ClientRegistry;
import org.lwjgl.input.Keyboard;

import java.lang.reflect.Field;

public class KeyBindings {
    private static final String CATEGORY = "key.radialmenu.category";

    public static final KeyBinding OPEN_MENU_0 = new KeyBinding("key.radialmenu.open_menu.0", KeyConflictContext.IN_GAME, Keyboard.KEY_R, CATEGORY);
    public static final KeyBinding EDIT_MENU_0 = new KeyBinding("key.radialmenu.edit_menu.0", KeyConflictContext.IN_GAME, KeyModifier.ALT, Keyboard.KEY_R, CATEGORY);

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
