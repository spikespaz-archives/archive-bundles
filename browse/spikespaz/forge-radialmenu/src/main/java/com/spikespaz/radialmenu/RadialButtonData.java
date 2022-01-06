package com.spikespaz.radialmenu;

import com.sun.istack.internal.NotNull;
import lombok.Getter;
import lombok.Setter;
import net.minecraft.client.resources.I18n;
import net.minecraft.client.settings.KeyBinding;

public class RadialButtonData {
    @Getter
    private KeyBinding keyBinding;
    @Getter
    @Setter
    private Object buttonIcon;
    @Getter
    @Setter
    private String name;
    @Getter
    @Setter
    private boolean toggleMode;

    public RadialButtonData(KeyBinding keyBinding, Object buttonIcon, @NotNull String name, boolean toggleMode) {
        this.keyBinding = keyBinding;
        this.buttonIcon = buttonIcon;
        this.name = name;
        this.toggleMode = toggleMode;
    }

    public RadialButtonData(KeyBinding keyBinding, Object buttonIcon, boolean toggleMode, Object unused) {
        this.setKeyBinding(keyBinding);
        this.buttonIcon = buttonIcon;
        this.toggleMode = toggleMode;
    }

    public void setKeyBinding(KeyBinding keyBinding) {
        this.keyBinding = keyBinding;
        if (keyBinding != null)
            this.name = I18n.format(keyBinding.getKeyDescription());
        else
            this.name = "";
    }
}
