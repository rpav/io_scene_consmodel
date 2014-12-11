# io_scene_consmodel

This is a **work-in-progress** plugin for exporting [Consmodel](https://github.com/rpav/consmodel) files from Blender 2.71+.

Installation and usage:

* Install this and [pyconspack](https://github.com/conspack/pyconspack) somewhere Blender can find them, i.e., your `$BLENDER_USER_SCRIPTS` directory, or more likely what "Scripts" is set to in "User Preferences" in the "File" tab.
* Follow [the usual method](http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Add-Ons) for enabling extensions.
* Once enabled, **press Spacebar for the Search dialog**, type "CMDL", and click "Export CMDL".

**THERE IS NO MENU ENTRY RIGHT NOW.**  There are no export options yet.  This is a work-in-progress, developed alongside Consmodel.  If you have no interest in following that development, this plugin is of no interest to you.

That said, development is progressing at a decent pace.  This currently has the following features:

* Cameras, point lights, meshes, and basic materials are exported.
* Hierarchy is preserved.
* Meshes are triangulated, normals are included.

Work is progressing toward:

* More light and material support
* Custom properties useful e.g. for tagging shader values right in Blenders
* Animations
* Textures

Current caveats:

* CMDL files are currently not as compact as possible.  The CONSPACK index for CMDL is not used, unused normal data is included, and probably some other less-than-optimal encoding is done.
* There's no menu entry or options; these are actually pretty easy, but not terribly useful for development.

Will not happen any time soon:

* Cycles material data.  In theory Consmodel can certainly contain this, I'm not sure it's useful for games, unless someone can point me at (or wants to write) a Cycles->GLSL converter that produces good real-time results.
* Non-mesh shapes.  Again, possible in theory, but of questionable usefulness.
* Importing.
