const wasmModulePromise = import(new URL("../wasm/datalink-wasm/datalink_wasm.js", import.meta.url).href)
  .then(async (module) => {
    await module.default({
      module_or_path: new URL("../wasm/datalink-wasm/datalink_wasm_bg.wasm", import.meta.url).href
    });
    if (module.run) module.run();
    return module;
  });

function safeDecode(decode) {
  return (raw, direction) => {
    try {
      return { ok: true, value: decode(raw, direction) };
    } catch (error) {
      return { ok: false, error: String(error?.message ?? error) };
    }
  };
}

export async function makeDatalinkHelpers({ htl, Inputs } = {}) {
  if (!htl) throw new Error("makeDatalinkHelpers requires the OJS htl object");
  const wasm = await wasmModulePromise;

  const jsonBlock = (value) => htl.html`<pre class="acars-json datalink-wasm-json"><code>${JSON.stringify(value, null, 2)}</code></pre>`;

  const errorBlock = (error, { application = "datalink message", direction = "" } = {}) => {
    const detail = String(error ?? "Unknown decoder error").replace(/^Error:\s*/, "");
    const directionText = direction ? ` ${direction}` : "";
    const article = /^[AEFHILMNORSX]/i.test(application) ? "an" : "a";
    return htl.html`<div role="alert" class="datalink-wasm-error-block">
      <strong>Could not decode this as ${article} ${application}${directionText}.</strong>
      <span>${detail}</span>
    </div>`;
  };

  const sampleButtons = (samples, label, {
    className = "datalink-sample-buttons",
    buttonLabel = (sample, index) => sample?.short ?? sample?.label ?? `Sample ${index + 1}`
  } = {}) => {
    let current = 0;
    const form = htl.html`<div class=${className} role="group" aria-label=${label}>
      ${samples.map((sample, index) => htl.html`<button type="button" data-index=${index}>${buttonLabel(sample, index)}</button>`)}
    </div>`;
    const setValue = (index, notify = true) => {
      current = index;
      for (const button of form.querySelectorAll("button")) {
        button.classList.toggle("active", +button.dataset.index === current);
      }
      if (notify) form.dispatchEvent(new Event("input", { bubbles: true }));
    };
    Object.defineProperty(form, "value", {
      get: () => current,
      set: (index) => setValue(+index, false)
    });
    form.addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (button) setValue(+button.dataset.index);
    });
    setValue(0, false);
    return form;
  };

  const envelopeInput = ({ value, ariaLabel, className = "datalink-envelope-input" } = {}) => {
    if (!Inputs) throw new Error("envelopeInput requires the OJS Inputs object");
    const control = Inputs.text({ value });
    control.classList.add(className);
    control.style.width = "100%";
    const input = control.querySelector("input");
    if (input) {
      input.style.width = "100%";
      if (ariaLabel) input.setAttribute("aria-label", ariaLabel);
      input.setAttribute("spellcheck", "false");
    }
    return control;
  };

  return {
    wasm,
    decodeAcars: safeDecode((raw, direction) => wasm.decode_acars(raw, direction)),
    decodeArinc622: safeDecode((raw, direction) => wasm.decode_arinc622(raw, direction)),
    jsonBlock,
    errorBlock,
    sampleButtons,
    envelopeInput
  };
}
