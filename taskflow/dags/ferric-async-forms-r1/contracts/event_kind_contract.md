# EventKind Contract

The walking skeleton declares the full `EventKind` enum set in `crates/ferric/src/vdom.rs`.
Feature spokes consume these variants but do not add new ones.

## Full EventKind Set

```rust
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub enum EventKind {
    // Mouse events
    Click,
    DblClick,
    MouseDown,
    MouseUp,
    MouseEnter,
    MouseLeave,
    MouseMove,
    MouseOver,
    MouseOut,
    ContextMenu,

    // Keyboard events
    KeyDown,
    KeyUp,
    KeyPress,

    // Input / focus events
    Input,
    Change,
    Focus,
    Blur,

    // Form events
    Submit,
    Reset,

    // Pointer events
    PointerDown,
    PointerUp,
    PointerEnter,
    PointerLeave,
    PointerMove,
    PointerCancel,

    // Scroll / resize
    Scroll,
    Resize,

    // Drag events
    DragStart,
    Drag,
    DragEnd,
    DragEnter,
    DragLeave,
    DragOver,
    Drop,

    // Touch events
    TouchStart,
    TouchEnd,
    TouchMove,
    TouchCancel,

    // Clipboard events
    Copy,
    Cut,
    Paste,

    // Animation / transition
    AnimationStart,
    AnimationEnd,
    AnimationIteration,
    TransitionEnd,

    // Load events
    Load,
    Error,

    // Custom escape hatch
    Custom(String),
}
```

## DOM Event String Mapping

Each variant must map to its DOM event string in the `dom.rs` binding layer:

| Variant        | DOM string          |
|----------------|---------------------|
| Click          | "click"             |
| DblClick       | "dblclick"          |
| MouseDown      | "mousedown"         |
| MouseUp        | "mouseup"           |
| MouseEnter     | "mouseenter"        |
| MouseLeave     | "mouseleave"        |
| MouseMove      | "mousemove"         |
| MouseOver      | "mouseover"         |
| MouseOut       | "mouseout"          |
| ContextMenu    | "contextmenu"       |
| KeyDown        | "keydown"           |
| KeyUp          | "keyup"             |
| KeyPress       | "keypress"          |
| Input          | "input"             |
| Change         | "change"            |
| Focus          | "focus"             |
| Blur           | "blur"              |
| Submit         | "submit"            |
| Reset          | "reset"             |
| PointerDown    | "pointerdown"       |
| PointerUp      | "pointerup"         |
| PointerEnter   | "pointerenter"      |
| PointerLeave   | "pointerleave"      |
| PointerMove    | "pointermove"       |
| PointerCancel  | "pointercancel"     |
| Scroll         | "scroll"            |
| Resize         | "resize"            |
| DragStart      | "dragstart"         |
| Drag           | "drag"              |
| DragEnd        | "dragend"           |
| DragEnter      | "dragenter"         |
| DragLeave      | "dragleave"         |
| DragOver       | "dragover"          |
| Drop           | "drop"              |
| TouchStart     | "touchstart"        |
| TouchEnd       | "touchend"          |
| TouchMove      | "touchmove"         |
| TouchCancel    | "touchcancel"       |
| Copy           | "copy"              |
| Cut            | "cut"               |
| Paste          | "paste"             |
| AnimationStart | "animationstart"    |
| AnimationEnd   | "animationend"      |
| AnimationIteration | "animationiteration" |
| TransitionEnd  | "transitionend"     |
| Load           | "load"              |
| Error          | "error"             |
| Custom(s)      | s.as_str()          |

## Binding Strategy (for SUBTASK_dom_events)

The existing `dom.rs` binding dispatch uses `match event_kind` to map each variant to a Closure.
SUBTASK_dom_events extends the `bind_events` function with the full set above.

The `Input` variant already has special handling (reads `input_element.value()`).
The `Change` variant should be treated identically to `Input` for HtmlInputElement targets.
All other variants call the `EventHandler` with `Fn()` — no event value is extracted.

NOTE: The `EventHandler = Rc<dyn Fn()>` type is currently zero-argument. Richer event data
(e.g., key code from KeyDown) is out of scope for this PR — callers who need key data
should use `Fn()` with signal closure capture for now. This keeps the type surface stable.
