# Rapid Prototyping Workflow

Sometimes teams need to experiment quickly before full documentation is written. Agent3D supports an optional workflow for this scenario.

1. **Prototype Branch**
   - Create a dedicated branch prefixed with `prototype/`.
   - Mark commits with the `experimental` tag to indicate temporary work.
2. **Minimal Documentation**
   - Record a brief description of the experiment in `docs/proposals/`.
   - Capture decisions and assumptions as they emerge.
3. **Retrospective Documentation**
   - Once the prototype proves valuable, expand the documentation to full Agent3D standards.
   - Run the Documentation Pass followed by Implementation and Testing Passes to bring the prototype into alignment.
4. **Cleanup**
   - Remove experimental branches that are no longer needed.
   - Ensure `docs/DDD-STATUS.md` reflects the updated state.

This workflow allows controlled experimentation without sacrificing the core principle that documentation leads production code.
