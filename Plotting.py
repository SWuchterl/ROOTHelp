import ROOT
import ROOTHelp

from ROOTHelp.Utils       import makeCanvas, set_max, set_min, setXMinMax
from ROOTHelp.PlotOptions import PlotOptions

def plot_hist_list(hists, **kw):
    draw_options      = kw.get('draw_options',   ['hist','hist'])
    x_min             = kw.get("x_min",             None)
    x_max             = kw.get("x_max",             None)
    y_title           = kw.get('y_title',           ROOTHelp.default)
    x_title           = kw.get('x_title',           ROOTHelp.default)

    #
    # Draw
    #
    for i, h in enumerate(hists):

        # draw
        if not draw_options:
            draw_options = ""
            
        if x_min or x_max:
            setXMinMax(h, x_min, x_max)
            
        if i:
            h.Draw(draw_options[i]+"same")    
        else:
            #h.Draw(draw_options)
            if not y_title == ROOTHelp.default:
                h.GetYaxis().SetTitle(y_title)
            if not x_title == ROOTHelp.default:
                h.GetXaxis().SetTitle(x_title)
            h.Draw(draw_options[i]+"PE")


    #
    #  Redraw the points
    #
    hists[0].Draw(draw_options[0]+"PEsame")
    hists[0].Draw(draw_options[0]+"sameaxis")


def config_hists(hists, **kw):

    #
    #  Read the congif
    #
    #title             = kw.get('title',             ROOTHelp.default)
    y_min             = kw.get('min',               None)
    y_max             = kw.get('max',               ROOTHelp.default)
    x_min             = kw.get("x_min",             None)
    x_max             = kw.get("x_max",             None)
    log_y             = kw.get('log_y',           False)

    fill_colors       = kw.get('fill_colors'  ,  [ROOT.kBlack,ROOT.kYellow,ROOT.kRed])
    fill_style        = kw.get('fill_style'  ,   [ROOTHelp.default,ROOTHelp.default])
    line_colors       = kw.get('line_colors'  ,  [ROOT.kBlack,ROOT.kBlack,ROOT.kRed])
    marker_styles     = kw.get('marker_styles',  [ROOTHelp.default,ROOTHelp.default,ROOTHelp.default])
    styles            = kw.get('styles'       ,  [ROOT.kSolid,ROOT.kSolid,ROOT.kSolid])
    widths            = kw.get('widths'       ,  [ROOTHelp.default, ROOTHelp.default,ROOTHelp.default])


    #
    #  Congigure the plots
    #
    for i, h in enumerate(hists):
        opt = dict() 
        opt['line_color']   = line_colors[i]
        opt['marker_color'] = line_colors[i]
        opt['line_style']   = styles[i]
        opt['line_width']   = widths[i]
        opt['fill_color']   = fill_colors[i]
        opt['fill_style']   = fill_style[i]
        opt['marker_style']   = marker_styles[i]
        plot_options = PlotOptions(**opt)
        plot_options.configure(h)


    #
    # Find the global min/max
    #
    set_min(hists, y_min, log_y=log_y)
    set_max(hists, y_max, log_y=log_y)


    #
    # Draw
    #
    for i, h in enumerate(hists):

        if x_min or x_max:
            setXMinMax(h, x_min, x_max)


    return {'hists':hists}
    


#
# Plot histsogram on top of each other 
#
def plot_hists( hists, name, **kw):
    """
    Function for formatting a list of histograms and plotting them on the same
    canvas, stacked. Returns a dictionary with the following keys:
    'canvas', 'stack', 'hists'.
    """

    #
    #  Read the congif
    #
    show_stats        = kw.get('show_stats',        False)

    #
    #  Config Hists
    #
    plot = config_hists(hists, **kw)

    #
    #  Build the canvas
    #
    c = makeCanvas(name,name, **kw)

    plot_hist_list(hists, **kw)

    # arrange stats
    if show_stats:
        c.Update()
        arrange_stats(hists)
    c.Update()
    return {'canvas':c, 'hists':hists}


#
#
#
def plot_shared_axis(top_hists, bottom_hists,name='',split=0.5
                     ,**kw):

    # options with defaults
    axissep       = kw.get('axissep'       ,0.0)
    ndivs         = kw.get('ndivs'           ,[503,503])
    rLabel        = kw.get("rlabel", "Ratio")
    rMin          = kw.get("rMin", 0)
    rMax          = kw.get("rMax", 2)
    bayesRatio    = kw.get('bayesRatio',     False)

    canvas = makeCanvas(name, name, width=600, height=600)
    top_pad    = ROOT.TPad("pad1", "The pad 80% of the height",0,split,1,1,0)
    bottom_pad = ROOT.TPad("pad2", "The pad 20% of the height",0,0,1,split,0)
    top_pad.Draw()
    bottom_pad.Draw()

    top_pad.cd()
    top_pad.SetLogy(kw.get('log_y', False))
    top_pad.SetTopMargin(canvas.GetTopMargin()*1.0/(1.0-split))
    top_pad.SetBottomMargin(0.5*axissep)
    top_pad.SetRightMargin(canvas.GetRightMargin())
    top_pad.SetLeftMargin(canvas.GetLeftMargin());
    top_pad.SetFillStyle(0) # transparent
    top_pad.SetBorderSize(0)
    plot_hist_list(top_hists, **kw)
    
    bottom_pad.cd()
    bottom_pad.SetTopMargin(2*axissep)
    bottom_pad.SetBottomMargin(canvas.GetBottomMargin()*1.0/split)
    bottom_pad.SetRightMargin(canvas.GetRightMargin())
    bottom_pad.SetLeftMargin(canvas.GetLeftMargin());
    bottom_pad.SetFillStyle(0) # transparent
    bottom_pad.SetBorderSize(0)
    ratio_axis = top_hists[0].Clone()
    ratio_axis.GetYaxis().SetTitle(rLabel)
    ratio_axis.GetXaxis().SetTitle(top_hists[0].GetXaxis().GetTitle())
    ratio_axis.GetYaxis().SetNdivisions(507)
    ratio_axis.GetYaxis().SetRangeUser(rMin, rMax)
    bottom_hists.GetYaxis().SetRangeUser(rMin, rMax)
    bottom_hists.GetYaxis().SetTitle(rLabel)
    

    if bayesRatio:
        ratio_axis.Draw("axis")
        bottom_hists.Draw("PE")
        ratio_axis.Draw("axis same")
    else:
        bottom_hists.Draw("PE")
        if ("sys_band" in kw) and (not kw["sys_band"] == None):  kw["sys_band"].Draw("E2 same")
        bottom_hists.Draw("PE same")
        oldSize = bottom_hists.GetMarkerSize()
        bottom_hists.SetMarkerSize(0)
        bottom_hists.DrawCopy("same e0")
        bottom_hists.SetMarkerSize(oldSize)
        bottom_hists.Draw("PE same")

    line = ROOT.TLine()
    line.DrawLine(top_hists[0].GetXaxis().GetXmin(), 1.0, top_hists[0].GetXaxis().GetXmax(), 1.0)

    pads = [top_pad, bottom_pad]
    factors = [0.8/(1.0-split), 0.7/split]
    for i_pad, pad in enumerate(pads):

        factor = factors[i_pad]
        ndiv   = ndivs[i_pad]
        
        prims = [ p.GetName() for p in pad.GetListOfPrimitives() ]
        
        #
        #  Protection for scaling hists multiple times
        #
        procedHist = []
        
        for name in prims:
            
            if name in procedHist: continue
            procedHist.append(name)
        
            h = pad.GetPrimitive(name)
            if isinstance(h, ROOT.TH1) or isinstance(h, ROOT.THStack) or isinstance(h, ROOT.TGraph) or isinstance(h, ROOT.TGraphErrors) or isinstance(h, ROOT.TGraphAsymmErrors):
                if isinstance(h, ROOT.TGraph) or isinstance(h, ROOT.THStack) or isinstance(h, ROOT.TGraphErrors) or isinstance(h, ROOT.TGraphAsymmErrors):
                    h = h.GetHistogram()
                #print "factor is",factor,h.GetName(),split
        
                if i_pad == 1:
                    h.SetLabelSize(h.GetLabelSize('Y')*factor, 'Y')
                    h.SetTitleSize(h.GetTitleSize('X')*factor, 'X')
                    h.SetTitleSize(h.GetTitleSize('Y')*factor, 'Y')
                    h.SetTitleOffset(h.GetTitleOffset('Y')/factor, 'Y')
                    
                if i_pad == 1:
                    h.GetYaxis().SetNdivisions(ndiv)
                h.GetXaxis().SetNdivisions()                
                if i_pad == 0:
                    h.SetLabelSize(0.0, 'X')
                    h.GetXaxis().SetTitle("")
                else:
                    h.SetLabelSize(h.GetLabelSize('X')*factor, 'X')
                    ## Trying to remove overlapping y-axis labels.  Doesn't work.
                    # h.GetYaxis().Set(4, h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax()) 
                    # h.GetYaxis().SetBinLabel( h.GetYaxis().GetLast(), '')

    return {'canvas':canvas,'ratio_axis':ratio_axis}



#
#
#
def makeBayesRatio(num, den):
    num.Sumw2()
    den.Sumw2()
    print "Doing Bayes Ratio"
    ratio = ROOT.TGraphAsymmErrors()#num.GetNbinsX())
    ratio.BayesDivide(num,den)
    ratio.SetName(num.GetName()+"_ratio")
    return ratio


#
#
#
def makeRatio(num, den):
    num.Sumw2()
    den.Sumw2()
    
    ratio = num.Clone(num.GetName()+"_ratio")
    ratio.Divide(den)
        
    debugRatioErrors = False
    if debugRatioErrors:
        xAxis = hists[0].GetXaxis()
        nBins = xAxis.GetNbins()
        for i in range(nBins):
            print "Bin",i
            print "\tnum",num.GetBinContent(i+1),"+/-",num.GetBinError(i+1)
            print "\tden",den.GetBinContent(i+1),"+/-",den.GetBinError(i+1)
            print "\trat",ratio.GetBinContent(i+1),"+/-",ratio.GetBinError(i+1)

    return ratio


#
#
#
def makeStatRatio(num, den, **kw):
    print "Doing Stats Ratio"

    mcscale        = kw.get('mcscale',       1.0)

    ratio_axis = num.Clone(num.GetName()+"_ratioaxis")
    ratio      = num.Clone(num.GetName()+"_ratio")
    ratio.Divide(den)

    xAxis = num.GetXaxis()
    nBins = xAxis.GetNbins()
    var_band   = ROOT.TGraphAsymmErrors(nBins)
    var_band.SetFillColor(ROOT.kRed)
    
    for i in range(nBins):

        #
        # Only use the numerator uncertianty in the ratio
        #
        newError = 0
        if num.GetBinContent(i):
            newError = ratio.GetBinContent(i)/pow(num.GetBinContent(i),0.5)

        ratio.SetBinError(i,newError)

        #
        # Use the scaled denominator uncertianty in the band
        #

        var_band.SetPoint(i,xAxis.GetBinCenter(i+1),1.0)


        error   = den.GetBinError(i+1)
        content = den.GetBinContent(i+1)

        relError = 0
        if content:
            relError = error/content * pow(mcscale,0.5)

        var_band.SetPointError(i,
                               xAxis.GetBinCenter(i+1)-xAxis.GetBinLowEdge(i+1),xAxis.GetBinUpEdge(i+1)-xAxis.GetBinCenter(i+1),
                               relError,relError)
    
    return ratio, var_band

#
#
#
def makeDenErrorBand(den, **kw):
    print "Doing Den Error Band"

    xAxis = den.GetXaxis()
    nBins = xAxis.GetNbins()
    var_band   = ROOT.TGraphAsymmErrors(nBins)
    var_band.SetFillColor(ROOT.kRed)
    
    for i in range(nBins):

        var_band.SetPoint(i,xAxis.GetBinCenter(i+1),1.0)

        error   = den.GetBinError(i+1)
        content = den.GetBinContent(i+1)

        relError = 0
        if content:
            relError = error/content

        var_band.SetPointError(i,
                               xAxis.GetBinCenter(i+1)-xAxis.GetBinLowEdge(i+1),xAxis.GetBinUpEdge(i+1)-xAxis.GetBinCenter(i+1),
                               relError,relError)
    
    return var_band


#
# Plot histsogram on top of each other 
#
def plot_hists_wratio( hists, name, **kw):
    """
    Function for formatting a list of histograms and plotting them on the same
    canvas, stacked. Returns a dictionary with the following keys:
    'canvas', 'stack', 'hists'.
    """

    #canvas_options = kw.get('canvas_options', ROOTHelp.default)
    logy           = kw.get('logy',     False)
    logx           = kw.get('logx',     False)
    bayesRatio     = kw.get('bayesRatio',     False)
    statRatio      = kw.get('statRatio',     False)
    showDenError   = kw.get('showDenError',     False)
    x_title = hists[0].GetXaxis().GetTitle()

    #
    #  Config Hists
    #
    plot = config_hists(hists, **kw)

    #
    #  make ratio
    #
    #num  = plot['hists'][0]
    #num.Sumw2()
    #den  = plot['hists'][1]
    #den.Sumw2()

    if bayesRatio:  
        plot["ratio"] = makeBayesRatio(num = plot['hists'][0].Clone(), den = plot['hists'][1].Clone())
    elif showDenError: 
        plot["ratio"] = makeRatio(num = plot['hists'][0].Clone(),  den = plot['hists'][1].Clone())
        var_band = makeDenErrorBand(den = plot['hists'][1].Clone(), **kw) 
        kw["sys_band"] = var_band
        plot["sys_band"] = var_band        
    elif statRatio: 
        ratio, var_band = makeStatRatio(num = plot['hists'][0].Clone(), den = plot['hists'][1].Clone(), **kw) 
        plot['ratio']  = ratio
        kw["sys_band"] = var_band
        plot["sys_band"] = var_band
    else:
        plot["ratio"] = makeRatio(num = plot['hists'][0].Clone(),  den = plot['hists'][1].Clone())



    #
    # draw ratio
    #
    shared = plot_shared_axis(plot['hists'],  plot['ratio'], name+"_with_ratio", split=0.3, axissep=0.02, ndivs=[505,503], **kw)

    plot['canvas']     = shared['canvas']
    plot['canvas'].Update()
    plot['ratio_axis'] = shared['ratio_axis']
    
    return plot