package com.spikespaz.radialmenu.gui;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import com.spikespaz.radialmenu.Utilities;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiButton;
import net.minecraft.client.gui.GuiScreen;
import net.minecraft.client.gui.GuiSlot;
import net.minecraft.client.resources.I18n;
import net.minecraft.client.settings.KeyBinding;

import java.io.IOException;
import java.util.List;
import java.util.Map;

public class GuiControlSelect extends GuiScreen {
    private final GuiScreen parentScreen;
    protected GuiButton buttonConfirm;
    protected KeyBinding selected;
    protected KeyBinding initialSelected;
    protected ControlList list;
    private Utilities.ICallback<KeyBinding> callback;

    public GuiControlSelect(Minecraft mc, GuiScreen parentScreen, Utilities.ICallback callback) {
        this.mc = mc;
        this.parentScreen = parentScreen;
        this.callback = callback;
    }

    public void initGui() {
        this.addButton(new GuiButton(200, this.width / 2 - 155 + 160, this.height - 29, 150, 20, I18n.format("gui.cancel")));
        this.buttonConfirm = this.addButton(new GuiButton(201, this.width / 2 - 155, this.height - 29, 150, 20, I18n.format("gui.radialmenu.button.confirm")));
        this.buttonConfirm.enabled = false;
        this.list = new ControlList(this.mc);
        this.list.registerScrollButtons(7, 8);
    }

    public void handleMouseInput() throws IOException {
        super.handleMouseInput();
        this.list.handleMouseInput();
    }

    protected void actionPerformed(GuiButton button) {
        if (button.enabled) {
            switch (button.id) {
                case 200: // Cancel
                    this.mc.displayGuiScreen(this.parentScreen);
                    break;
                case 201: // Done
                    this.confirmSelection();
                    break;
                default:
                    this.list.actionPerformed(button);
            }
        }
    }

    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        this.list.drawScreen(mouseX, mouseY, partialTicks);
        this.drawCenteredString(this.fontRenderer, I18n.format("controls.title"), this.width / 2, 16, 16777215);
        super.drawScreen(mouseX, mouseY, partialTicks);
    }

    public void confirmSelection() {
        this.callback.resolve(this.selected);
        this.mc.displayGuiScreen(this.parentScreen);

        if (this.parentScreen == null)
            this.mc.setIngameFocus();
    }

    public void setSelected(KeyBinding binding) {
        this.selected = binding;
        this.buttonConfirm.enabled = !binding.equals(this.initialSelected);
    }

    public void setInitialSelected(KeyBinding binding) {
        this.initialSelected = binding;
        this.setSelected(binding);
    }

    class ControlList extends GuiSlot {
        private final List<String> listStrings = Lists.newArrayList();
        private final List<String> listCategories = Lists.newArrayList();
        private final Map<String, KeyBinding> keyBindMap = Maps.newHashMap();

        public ControlList(Minecraft mc) {
            super(mc, GuiControlSelect.this.width, GuiControlSelect.this.height, 32, GuiControlSelect.this.height - 39, 18);

            for (KeyBinding binding : mc.gameSettings.keyBindings) {
                if (!listStrings.contains(binding.getKeyCategory())) {
                    listCategories.add(binding.getKeyCategory());
                    listStrings.add(binding.getKeyCategory());
                }

                listStrings.add(binding.getKeyDescription());
                keyBindMap.put(binding.getKeyDescription(), binding);
            }
        }

        protected int getSize() {
            return this.keyBindMap.size();
        }

        protected void elementClicked(int slotIndex, boolean isDoubleClick, int mouseX, int mouseY) {
            if (listCategories.contains(this.listStrings.get(slotIndex)))
                return;

            if (isDoubleClick) {
                GuiControlSelect.this.buttonConfirm.playPressSound(mc.getSoundHandler());
                GuiControlSelect.this.confirmSelection();
            } else
                GuiControlSelect.this.setSelected(this.keyBindMap.get(this.listStrings.get(slotIndex)));
        }

        protected boolean isSelected(int slotIndex) {
            if (GuiControlSelect.this.selected == null)
                return false;

            return listStrings.indexOf(GuiControlSelect.this.selected.getKeyDescription()) == slotIndex;
        }

        protected int getContentHeight() {
            return this.getSize() * 18;
        }

        protected void drawBackground() {
            GuiControlSelect.this.drawDefaultBackground();
        }

        protected void drawSlot(int slotIndex, int posX, int posY, int height, int mouseX, int mouseY, float partialTicks) {
            final String keyName = this.listStrings.get(slotIndex);
            final int color = listCategories.contains(keyName) ? 0xFFD9A334 : 0xFFFFFFFF;

            GuiControlSelect.this.drawCenteredString(GuiControlSelect.this.fontRenderer, I18n.format(keyName), this.width / 2, posY + 1, color);
        }
    }
}