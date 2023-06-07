from json import loads as jsn

def _convert_stylesheet(theme_list, theme_folder, themeindex):
    # Loading theme stylesheet
    f   = theme_list[themeindex]['file']
    vf  = theme_list[themeindex]['varfile']
    n   = theme_list[themeindex]['name']
    opt = theme_list[themeindex]['opt']

    if opt == "":
        o = False
    else:
        o = True

    varsf = open(theme_folder + vf, 'r').read()
    varsf = jsn(varsf)

    style = open(theme_folder + f, 'r').read()

    if o:
        style_opt = open(theme_folder + opt, 'r').read()
    
    for var in varsf: # Replacing vars in variable file
        style = style.replace(var, varsf[var])

        if o:
            style_opt = style_opt.replace(var, varsf[var])

    if o:
        return style + "\n" + style_opt
    else:
        return style