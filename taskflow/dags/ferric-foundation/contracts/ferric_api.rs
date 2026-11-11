// contracts/ferric_api.rs — FROZEN public API surface of the `ferric` crate.
// Kind: rust_trait. READ-ONLY for every descendant task. This is a reference artifact, not a
// compiled crate member: implementers MATCH these signatures in crates/ferric/src/<module>.rs.
//
// WHAT IS FROZEN (binding): the module layout, the set of public items named below, their roles,
// and the prelude re-export surface. These are the cross-layer seam and the surface later
// work-items (ferric-router, chirp-frontend) will depend on. Changing a frozen public signature
// requires an ADDITIVE plan amendment — not an in-place edit.
//
// WHAT IS LATITUDE (owner's design): all private/internal types and representations — the reactive
// runtime's storage (arena / slotmap / Rc-RefCell), the concrete `Patch` variants, the internal
// fields of `VElement`, scope/cleanup machinery. Owners may refine these freely. If a *public*
// signature below proves wrong, request an additive amendment; do not deviate silently.
//
// Dependency crates (declared by scaffold in crates/ferric/Cargo.toml): wasm-bindgen, web-sys,
// js-sys. Keep deps lean — we are BUILDING a framework.

// =====================================================================================
// module: signal            owner: SUBTASK_reactive_core        file: src/signal.rs
// Fine-grained reactivity (Solid/Leptos-style). A `Signal` is a cheap Copy handle into a
// reactive runtime. Reads inside a reactive context (an effect / memo) subscribe automatically;
// writes notify subscribers. `batch` coalesces notifications; dropped effects must unsubscribe
// (soundness identity `no_stale_subscriber_leak`).
// =====================================================================================

/// A readable+writable reactive value handle. Cheap to Clone/Copy (it is a key into the runtime).
pub struct Signal<T: 'static> { /* owner-designed: runtime key + PhantomData<T> */ }

impl<T: 'static> Clone for Signal<T> { /* ... */ }
impl<T: 'static> Copy for Signal<T> {}

impl<T: 'static> Signal<T> {
    /// Read the value, cloning it out. Subscribes the current reactive observer (if any).
    pub fn get(&self) -> T where T: Clone { todo!() }
    /// Read by reference without cloning. Subscribes the current reactive observer (if any).
    pub fn with<R>(&self, f: impl FnOnce(&T) -> R) -> R { todo!() }
    /// Replace the value and notify subscribers.
    pub fn set(&self, value: T) { todo!() }
    /// Mutate the value in place and notify subscribers.
    pub fn update(&self, f: impl FnOnce(&mut T)) { todo!() }
}

/// Create a reactive signal with an initial value.
pub fn create_signal<T: 'static>(value: T) -> Signal<T> { todo!() }

/// A derived/computed value. Recomputes lazily when its reactive dependencies change; memoizes.
pub struct Memo<T: 'static> { /* owner-designed */ }

impl<T: 'static> Clone for Memo<T> { /* ... */ }
impl<T: 'static> Copy for Memo<T> {}

impl<T: 'static> Memo<T> {
    pub fn get(&self) -> T where T: Clone { todo!() }
    pub fn with<R>(&self, f: impl FnOnce(&T) -> R) -> R { todo!() }
}

/// Create a memoized derived value from a closure that reads other signals/memos.
pub fn create_memo<T: 'static>(f: impl Fn() -> T + 'static) -> Memo<T> { todo!() }

/// Register a reactive side effect. Runs once immediately (tracking its signal reads), then
/// re-runs whenever any tracked dependency changes. The DOM runtime builds re-render on this.
pub fn create_effect(f: impl FnMut() + 'static) { todo!() }

/// Run `f`, coalescing all signal notifications into a single flush at the end (batched update).
pub fn batch<R>(f: impl FnOnce() -> R) -> R { todo!() }

// =====================================================================================
// module: vdom              owner: SUBTASK_view_and_diff        file: src/vdom.rs
// The view tree a component renders, plus the keyed diff. `Patch` is CONSUMED by the DOM runtime
// (src/dom.rs) to mutate real DOM — it is a cross-layer type, but the view→dom edge is SERIALIZED,
// so the runtime reads the REAL `Patch` enum; its variants are the owner's design (not frozen).
// =====================================================================================

/// A node in the view tree: an element or a text node.
pub enum VNode {
    Element(VElement),
    Text(String),
}

/// An element node. Field set is owner-designed beyond what is named here; `key` MUST exist to
/// support keyed diffing of child lists.
pub struct VElement {
    pub tag: String,
    pub key: Option<Key>,
    pub attrs: Vec<(String, String)>,
    pub events: Vec<(EventKind, EventHandler)>,
    pub children: Vec<VNode>,
}

/// Stable identity for keyed list diffing.
pub type Key = String;

/// Events the framework binds (acceptance criteria require at least click + input).
pub enum EventKind { Click, Input }

/// A boxed event callback. Concrete wrapper type is owner-designed (e.g. Rc<dyn Fn(web_sys::Event)>).
pub type EventHandler = std::rc::Rc<dyn Fn(/* web_sys::Event */)>;

/// A single patch operation produced by the keyed diff. Variants are owner-designed.
pub enum Patch { /* owner-designed: ReplaceText, SetAttr, RemoveAttr, InsertChild{key}, MoveChild, RemoveChild, ... */ }

/// Compute the minimal keyed patch list to turn `old` into `new`. Pure + native-testable.
pub fn diff(old: &VNode, new: &VNode) -> Vec<Patch> { todo!() }

// =====================================================================================
// module: component         owner: SUBTASK_view_and_diff        file: src/component.rs
// The component abstraction producing a view tree. Trait AND function-component support.
// =====================================================================================

/// A component renders itself to a view tree. `render` is re-invoked by the runtime (inside an
/// effect) when the signals it reads change.
pub trait Component {
    fn render(&self) -> VNode;
}

/// Function components: any `Fn() -> VNode` is a Component.
impl<F> Component for F where F: Fn() -> VNode {
    fn render(&self) -> VNode { (self)() }
}

// =====================================================================================
// module: dom               owner: SUBTASK_dom_runtime          file: src/dom.rs
// The browser runtime. Renders a component's view tree into a real DOM element via
// wasm-bindgen + web-sys, re-rendering via a keyed patch when signals change, and binds events.
// =====================================================================================

/// Mount `component` into the real DOM element `root`, render it, and keep it reactively updated:
/// the runtime wraps rendering in `create_effect`, so a signal change re-renders and applies the
/// keyed `diff`/`Patch` to the live DOM. Event handlers from the view tree are bound to DOM events.
pub fn mount(/* root: web_sys::Element, */ component: impl Component + 'static) { todo!() }

// =====================================================================================
// module: prelude           owner: SUBTASK_scaffold (re-exports)  file: src/lib.rs
// The frozen public surface. `use ferric::prelude::*;` MUST bring the following into scope:
//   Signal, create_signal, Memo, create_memo, create_effect, batch,   (from signal)
//   VNode, VElement, EventKind, Component,                            (from vdom + component)
//   mount,                                                            (from dom)
// plus any convenience builders the owners add (additive). This list is the `public_api_surface`
// identity the synthesis gate asserts.
// =====================================================================================
