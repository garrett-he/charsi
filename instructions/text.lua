RegisterInstruction("Text", function(origin, text)
    return text:gsub("\\n", "\n")
end)
