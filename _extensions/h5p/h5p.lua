-- {{< h5p name >}} embeds the H5P content extracted to h5p/content/<name>/
-- (see h5p/extract-h5p.ps1). Optional: title="..." for the PDF placeholder.
-- HTML: an empty div that h5p-loader.html fills with the h5p-standalone player.
-- Other formats (PDF): a short note pointing to the online version.

local loader_added = false

return {
  ["h5p"] = function(args, kwargs, meta)
    local name = pandoc.utils.stringify(args[1] or "")
    -- keep folder names URL- and attribute-safe
    name = name:gsub("[^%w%-_]", "")
    if name == "" then
      quarto.log.warning("h5p shortcode: missing content name")
      return pandoc.Null()
    end

    if quarto.doc.is_format("html:js") then
      if not loader_added then
        quarto.doc.include_file("after-body", "h5p-loader.html")
        loader_added = true
      end
      return pandoc.RawBlock("html",
        '<div class="h5p-embed" data-h5p="' .. name .. '"></div>')
    end

    local title = pandoc.utils.stringify(kwargs["title"] or "")
    if title == "" then title = "Interactive exercise" end
    return pandoc.Para({
      pandoc.Emph(pandoc.Str(title .. ": available in the online version of this script."))
    })
  end
}
