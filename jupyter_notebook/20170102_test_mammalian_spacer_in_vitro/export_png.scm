;gimp -i -b "$(cat export_png.scm)" 20170110_transcribe_cf_sgrnas.xcf
(define image (car (gimp-image-duplicate 1)))
(define layer (car (gimp-image-merge-visible-layers image CLIP-TO-IMAGE)))
(file-png-save-defaults
  RUN-NONINTERACTIVE image layer "export_png.png" "")
(gimp-image-delete image)
(gimp-quit 1)

