(() => {
    const form = document.getElementById("designForm");
    const frame = document.getElementById("previewFrame");
    if (!form || !frame) return;

    const paintSwatch = document.getElementById("previewPaintSwatch");
    const paintLabel = document.getElementById("previewPaintLabel");
    const graphic = document.getElementById("previewGraphic");
    const spoiler = document.getElementById("previewSpoiler");
    const selections = document.getElementById("previewSelections");
    const fields = {
        color: document.getElementById("id_color"),
        wheels: document.getElementById("id_wheels"),
        spoiler: document.getElementById("id_spoiler"),
        stickers: document.getElementById("id_stickers"),
        exhaust: document.getElementById("id_exhaust"),
    };
    const labels = {
        color: "Paint",
        wheels: "Wheels",
        spoiler: frame.closest(".customizer").dataset.category === "bike" ? "Tail" : "Spoiler",
        stickers: "Graphics",
        exhaust: "Exhaust",
    };

    const selectedLabel = (field) => {
        if (!field) return "";
        const option = field.options[field.selectedIndex];
        return option ? option.textContent.trim() : "";
    };

    function updatePreview() {
        // Keep the catalog photograph untouched; paint is shown as a swatch.
        if (fields.color && paintSwatch) paintSwatch.style.backgroundColor = fields.color.value;
        if (fields.color && paintLabel) paintLabel.textContent = selectedLabel(fields.color);
        if (fields.stickers && graphic) {
            graphic.dataset.style = fields.stickers.value;
            graphic.textContent = fields.stickers.value === "number" ? "07" : "";
        }
        if (fields.spoiler && spoiler) spoiler.dataset.style = fields.spoiler.value;
        if (fields.wheels) frame.dataset.wheel = selectedLabel(fields.wheels);
        if (fields.exhaust) frame.dataset.exhaust = selectedLabel(fields.exhaust);

        selections.replaceChildren();
        Object.entries(fields).forEach(([key, field]) => {
            if (!field) return;
            const chip = document.createElement("span");
            chip.className = "selection-chip";
            if (key === "color") {
                const swatch = document.createElement("i");
                swatch.className = "selection-swatch";
                swatch.style.backgroundColor = field.value;
                chip.append(swatch);
            }
            chip.append(`${labels[key]}: ${selectedLabel(field)}`);
            selections.append(chip);
        });

        form.querySelectorAll('input[name="accessories"]:checked').forEach((input) => {
            const chip = document.createElement("span");
            chip.className = "selection-chip selection-chip-accessory";
            const label = form.querySelector(`label[for="${input.id}"]`);
            chip.textContent = `+ ${label ? label.textContent.trim() : input.value}`;
            selections.append(chip);
        });
    }

    form.addEventListener("change", updatePreview);
    updatePreview();
})();
