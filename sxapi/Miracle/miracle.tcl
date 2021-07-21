#############################################################################
# Generated by PAGE version 6.2
#  in conjunction with Tcl version 8.6
#  Jul 21, 2021 10:28:06 AM CEST  platform: Windows NT
set vTcl(timestamp) ""
if {![info exists vTcl(borrow)]} {
    tk_messageBox -title Error -message  "You must open project files from within PAGE."
    exit}


if {!$vTcl(borrow) && !$vTcl(template)} {

set vTcl(actual_gui_font_dft_desc)  TkDefaultFont
set vTcl(actual_gui_font_dft_name)  TkDefaultFont
set vTcl(actual_gui_font_text_desc)  TkTextFont
set vTcl(actual_gui_font_text_name)  TkTextFont
set vTcl(actual_gui_font_fixed_desc)  TkFixedFont
set vTcl(actual_gui_font_fixed_name)  TkFixedFont
set vTcl(actual_gui_font_menu_desc)  TkMenuFont
set vTcl(actual_gui_font_menu_name)  TkMenuFont
set vTcl(actual_gui_font_tooltip_desc)  TkDefaultFont
set vTcl(actual_gui_font_tooltip_name)  TkDefaultFont
set vTcl(actual_gui_font_treeview_desc)  TkDefaultFont
set vTcl(actual_gui_font_treeview_name)  TkDefaultFont
set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #ececec
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(actual_gui_menu_active_fg)  #000000
set vTcl(pr,autoalias) 1
set vTcl(pr,relative_placement) 1
set vTcl(mode) Relative
}




proc vTclWindow.top44 {base} {
    global vTcl
    if {$base == ""} {
        set base .top44
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 236x211+691+-907
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 3204 2261
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "Miracle"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    set vTcl(real_top) {}
    vTcl:withBusyCursor {
    button $top.but45 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command doPressed \
        -disabledforeground #a3a3a3 -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Do 
    vTcl:DefineAlias "$top.but45" "Button1" vTcl:WidgetProc "Toplevel1" 1
    button $top.but46 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command rePressed \
        -disabledforeground #a3a3a3 -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text Re 
    vTcl:DefineAlias "$top.but46" "Button2" vTcl:WidgetProc "Toplevel1" 1
    button $top.but47 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command miPressed \
        -disabledforeground #a3a3a3 -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text {Mi !} 
    vTcl:DefineAlias "$top.but47" "Button3" vTcl:WidgetProc "Toplevel1" 1
    button $top.but49 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command runPressed \
        -disabledforeground #a3a3a3 -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text {Run !} 
    vTcl:DefineAlias "$top.but49" "Button4" vTcl:WidgetProc "Toplevel1" 1
    button $top.but50 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command stopPressed \
        -disabledforeground #a3a3a3 -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text {Stop !} 
    vTcl:DefineAlias "$top.but50" "Button5" vTcl:WidgetProc "Toplevel1" 1
    ttk::scale $top.tSc52 \
        -orient vertical -from 6000 -to 0 -length 91 -variable rpm_gui -takefocus {} 
    vTcl:DefineAlias "$top.tSc52" "TScale1" vTcl:WidgetProc "Toplevel1" 1
    scale $top.sca53 \
        -activebackground $vTcl(analog_color_m) \
        -background $vTcl(actual_gui_bg) -bigincrement 0.0 \
        -foreground $vTcl(actual_gui_fg) -from 60.0 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -length 96 -resolution 1.0 -variable iref_gui -tickinterval 0.0 -to 0.0 \
        -troughcolor #d9d9d9 
    vTcl:DefineAlias "$top.sca53" "Scale2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab54 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text iref 
    vTcl:DefineAlias "$top.lab54" "Label1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab55 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text RPM 
    vTcl:DefineAlias "$top.lab55" "Label2" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.but45 \
        -in $top -x 0 -relx 0.085 -y 0 -rely 0.711 -width 57 -relwidth 0 \
        -height 44 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but46 \
        -in $top -x 0 -relx 0.381 -y 0 -rely 0.711 -width 57 -relwidth 0 \
        -height 44 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but47 \
        -in $top -x 0 -relx 0.678 -y 0 -rely 0.711 -width 57 -relwidth 0 \
        -height 44 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but49 \
        -in $top -x 0 -relx 0.339 -y 0 -rely 0.142 -width 77 -relwidth 0 \
        -height 34 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but50 \
        -in $top -x 0 -relx 0.339 -y 0 -rely 0.379 -width 77 -relwidth 0 \
        -height 34 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tSc52 \
        -in $top -x 0 -relx 0.763 -y 0 -rely 0.095 -width 26 -relwidth 0 \
        -height 0 -relheight 0.431 -anchor nw -bordermode ignore 
    place $top.sca53 \
        -in $top -x 0 -relx 0.085 -y 0 -rely 0.095 -width 45 -relwidth 0 \
        -height 0 -relheight 0.455 -anchor nw -bordermode ignore 
    place $top.lab54 \
        -in $top -x 0 -relx 0.127 -y 0 -rely 0.569 -width 0 -relwidth 0.144 \
        -height 0 -relheight 0.09 -anchor nw -bordermode ignore 
    place $top.lab55 \
        -in $top -x 0 -relx 0.763 -y 0 -rely 0.569 -width 0 -relwidth 0.144 \
        -height 0 -relheight 0.09 -anchor nw -bordermode ignore 
    } ;# end vTcl:withBusyCursor 

    vTcl:FireEvent $base <<Ready>>
}



set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top44 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}

