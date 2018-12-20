__all__ = ['neb_calc_tm']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['NEB'])
Js('use strict')
@Js
def PyJs_anonymous_0_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['b', 'a'])
    PyJs_Object_1_ = Js({'redirectTo':Js('/')})
    def PyJs_LONG_19_(var=var):
        PyJs_Object_2_ = Js({'templateUrl':Js('views/about.204cf15b.html'),'controller':Js('AboutCtrl'),'controllerAs':Js('about')})
        PyJs_Object_3_ = Js({'templateUrl':Js('views/about.204cf15b.html'),'controller':Js('AboutCtrl'),'controllerAs':Js('about')})
        @Js
        def PyJs_anonymous_6_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return var.get('a').get('promise')
        PyJs_anonymous_6_._set_name('anonymous')
        PyJs_Object_5_ = Js({'dataloaded':Js([Js('tmcalculatorData'), PyJs_anonymous_6_])})
        PyJs_Object_4_ = Js({'templateUrl':Js('views/main.9b69837c.html'),'controller':Js('MainCtrl'),'resolve':PyJs_Object_5_})
        @Js
        def PyJs_anonymous_9_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return var.get('a').get('promise')
        PyJs_anonymous_9_._set_name('anonymous')
        PyJs_Object_8_ = Js({'dataloaded':Js([Js('tmcalculatorData'), PyJs_anonymous_9_])})
        PyJs_Object_7_ = Js({'templateUrl':Js('views/main.9b69837c.html'),'controller':Js('MainCtrl'),'resolve':PyJs_Object_8_})
        @Js
        def PyJs_anonymous_12_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return var.get('a').get('promise')
        PyJs_anonymous_12_._set_name('anonymous')
        PyJs_Object_11_ = Js({'dataloaded':Js([Js('tmcalculatorData'), PyJs_anonymous_12_])})
        PyJs_Object_10_ = Js({'templateUrl':Js('views/batch.03c23ef3.html'),'controller':Js('BatchCtrl'),'resolve':PyJs_Object_11_})
        PyJs_Object_13_ = Js({'templateUrl':Js('views/help.ef501d45.html'),'controller':Js('AboutCtrl')})
        PyJs_Object_14_ = Js({'templateUrl':Js('views/about.204cf15b.html'),'controller':Js('AboutCtrl')})
        PyJs_Object_15_ = Js({'templateUrl':Js('views/testbs.html'),'controller':Js('TestbsCtrl')})
        @Js
        def PyJs_anonymous_18_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return var.get('a').get('promise')
        PyJs_anonymous_18_._set_name('anonymous')
        PyJs_Object_17_ = Js({'dataloaded':Js([Js('tmcalculatorData'), PyJs_anonymous_18_])})
        PyJs_Object_16_ = Js({'templateUrl':Js('views/main.9b69837c.html'),'controller':Js('MainCtrl'),'resolve':PyJs_Object_17_})
        return var.get('a').callprop('when', Js('/'), PyJs_Object_16_).callprop('when', Js('/testbs'), PyJs_Object_15_).callprop('when', Js('/about'), PyJs_Object_14_).callprop('when', Js('/help'), PyJs_Object_13_).callprop('when', Js('/batch'), PyJs_Object_10_).callprop('when', Js('/:p1seq/:p2seq'), PyJs_Object_7_).callprop('when', Js('/:p1seq'), PyJs_Object_4_).callprop('when', Js('/about'), PyJs_Object_3_).callprop('when', Js('/about'), PyJs_Object_2_)
    PyJsComma(var.get('b').callprop('html5Mode', Js(1.0).neg()),PyJs_LONG_19_().callprop('otherwise', PyJs_Object_1_))
PyJs_anonymous_0_._set_name('anonymous')
@Js
def PyJs_anonymous_20_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a'])
    PyJsComma(var.get('a').callprop('html5Mode', Js(1.0).neg()),var.get('a').callprop('hashPrefix', Js('!')))
PyJs_anonymous_20_._set_name('anonymous')
def PyJs_LONG_40_(var=var):
    @Js
    def PyJs_anonymous_21_(a, this, arguments, var=var):
        var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
        var.registers(['a'])
        @Js
        def PyJs_anonymous_23_(b, c, d, this, arguments, var=var):
            var = Scope({'b':b, 'c':c, 'd':d, 'this':this, 'arguments':arguments}, var)
            var.registers(['b', 'c', 'd', 'e'])
            var.put('e', var.get('a')(var.get('d').get('onReadFile')))
            @Js
            def PyJs_anonymous_24_(a, this, arguments, var=var):
                var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
                var.registers(['c', 'a'])
                var.put('c', var.get('FileReader').create())
                @Js
                def PyJs_anonymous_25_(a, this, arguments, var=var):
                    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
                    var.registers(['a'])
                    @Js
                    def PyJs_anonymous_26_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments}, var)
                        var.registers([])
                        PyJs_Object_27_ = Js({'filedata':var.get('a').get('target').get('result')})
                        var.get('e')(var.get('b'), PyJs_Object_27_)
                    PyJs_anonymous_26_._set_name('anonymous')
                    var.get('b').callprop('$apply', PyJs_anonymous_26_)
                PyJs_anonymous_25_._set_name('anonymous')
                PyJsComma(var.get('c').put('onload', PyJs_anonymous_25_),var.get('c').callprop('readAsText', (var.get('a').get('srcElement') or var.get('a').get('target')).get('files').get('0')))
            PyJs_anonymous_24_._set_name('anonymous')
            var.get('c').callprop('on', Js('change'), PyJs_anonymous_24_)
        PyJs_anonymous_23_._set_name('anonymous')
        PyJs_Object_22_ = Js({'restrict':Js('A'),'scope':Js(1.0).neg(),'link':PyJs_anonymous_23_})
        return PyJs_Object_22_
    PyJs_anonymous_21_._set_name('anonymous')
    @Js
    def PyJs_anonymous_28_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        PyJs_Object_30_ = Js({'processwith':Js('&')})
        @Js
        def PyJs_anonymous_31_(a, b, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'b', 'd', 'a', 'e'])
            var.put('c', var.get('angular').callprop('element', var.get('b').callprop('children').callprop('eq', Js(1.0))))
            @Js
            def PyJs_anonymous_32_(a, this, arguments, var=var):
                var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
                var.registers(['a'])
                PyJsComma(PyJsComma(var.get('a').callprop('stopPropagation'),var.get('a').callprop('preventDefault')),var.get('a').get('dataTransfer').put('dropEffect', Js('copy')))
            PyJs_anonymous_32_._set_name('anonymous')
            var.put('d', PyJs_anonymous_32_)
            @Js
            def PyJs_anonymous_33_(b, this, arguments, var=var):
                var = Scope({'b':b, 'this':this, 'arguments':arguments}, var)
                var.registers(['b', 'c'])
                var.put('c', var.get('FileReader').create())
                @Js
                def PyJs_anonymous_34_(b, this, arguments, var=var):
                    var = Scope({'b':b, 'this':this, 'arguments':arguments}, var)
                    var.registers(['b'])
                    PyJs_Object_35_ = Js({'filedata':var.get('b').get('target').get('result')})
                    PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('console').callprop('log', Js('about to call processwith')),var.get('console').callprop('log', var.get('b').get('target').get('result'))),var.get('console').callprop('log', var.get('a').get('processwith'))),var.get('a').callprop('processwith', PyJs_Object_35_)),var.get('console').callprop('log', Js('after call to processwith')))
                PyJs_anonymous_34_._set_name('anonymous')
                PyJsComma(var.get('c').put('onload', PyJs_anonymous_34_),var.get('c').callprop('readAsText', (var.get('b').get('srcElement') or var.get('b').get('target')).get('files').get('0')))
            PyJs_anonymous_33_._set_name('anonymous')
            var.put('e', PyJs_anonymous_33_)
            PyJsComma(PyJsComma(var.get('c').callprop('on', Js('dragover'), var.get('d')),var.get('c').callprop('on', Js('drop'), var.get('e'))),var.get('c').callprop('on', Js('change'), var.get('e')))
        PyJs_anonymous_31_._set_name('anonymous')
        PyJs_Object_29_ = Js({'restrict':Js('A'),'replace':Js(0.0).neg(),'scope':PyJs_Object_30_,'template':Js('<div><div></div><input type="file" /></div>'),'link':PyJs_anonymous_31_})
        return PyJs_Object_29_
    PyJs_anonymous_28_._set_name('anonymous')
    @Js
    def PyJs_anonymous_36_(a, b, c, this, arguments, var=var):
        var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
        var.registers(['b', 'c', 'a'])
        @Js
        def PyJs_anonymous_37_(a, b, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
            var.registers(['b', 'd', 'a'])
            PyJs_Object_38_ = Js({'templateUrl':((Js('views/modals/')+var.get('a'))+Js('.html')),'size':var.get('b')})
            var.put('d', PyJs_Object_38_)
            PyJs_Object_39_ = Js({})
            var.get('c').callprop('showModal', var.get('d'), PyJs_Object_39_)
        PyJs_anonymous_37_._set_name('anonymous')
        PyJsComma(PyJsComma(var.get('jQuery').get('event').get('props').callprop('push', Js('dataTransfer')),var.get('a').put('appVersion', Js('1.9.5'))),var.get('a').put('openmodal', PyJs_anonymous_37_))
    PyJs_anonymous_36_._set_name('anonymous')
    return var.get('angular').callprop('module', Js('tmcApp'), Js([Js('ngAnimate'), Js('ngCookies'), Js('ngResource'), Js('ngRoute'), Js('ngSanitize'), Js('ngTouch'), Js('ui.bootstrap')])).callprop('run', Js([Js('$rootScope'), Js('$modal'), Js('modalService'), PyJs_anonymous_36_])).callprop('directive', Js('fileinput'), PyJs_anonymous_28_).callprop('directive', Js('onReadFile'), Js([Js('$parse'), PyJs_anonymous_21_]))
@Js
def PyJs_anonymous_41_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['c', 'b', 'd', 'a', 'e'])
    PyJs_Object_42_ = Js({'backdrop':Js(0.0).neg(),'keyboard':Js(0.0).neg(),'modalFade':Js(0.0).neg()})
    var.put('c', PyJs_Object_42_)
    PyJs_Object_43_ = Js({})
    var.put('d', PyJs_Object_43_)
    PyJs_Object_44_ = Js({})
    var.put('e', PyJs_Object_44_)
    @Js
    def PyJs_anonymous_45_(a, b, this, arguments, var=var):
        var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
        var.registers(['b', 'a'])
        PyJs_Object_46_ = Js({})
        return PyJsComma(PyJsComma((var.get('a') or var.put('a', PyJs_Object_46_)),var.get('a').put('backdrop', Js(0.0).neg())),var.get(u"this").callprop('show', var.get('a'), var.get('b')))
    PyJs_anonymous_45_._set_name('anonymous')
    @Js
    def PyJs_anonymous_47_(a, e, this, arguments, var=var):
        var = Scope({'a':a, 'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['e', 'g', 'a', 'f'])
        PyJs_Object_48_ = Js({})
        var.put('f', PyJs_Object_48_)
        PyJs_Object_49_ = Js({})
        var.put('g', PyJs_Object_49_)
        @Js
        def PyJs_anonymous_50_(a, b, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
            var.registers(['b', 'a'])
            @Js
            def PyJs_anonymous_51_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('b').callprop('close', Js('done'))
            PyJs_anonymous_51_._set_name('anonymous')
            @Js
            def PyJs_anonymous_52_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('b').callprop('close', Js('done'))
            PyJs_anonymous_52_._set_name('anonymous')
            PyJsComma(PyJsComma(var.get('a').put('modalOptions', var.get('g')),var.get('a').get('modalOptions').put('close', PyJs_anonymous_51_)),var.get('a').get('modalOptions').put('ok', PyJs_anonymous_52_))
        PyJs_anonymous_50_._set_name('anonymous')
        return PyJsComma(PyJsComma(PyJsComma(var.get('angular').callprop('extend', var.get('f'), var.get('c'), var.get('a')),var.get('angular').callprop('extend', var.get('g'), var.get('d'), var.get('e'))),(var.get('f').get('controller') or var.get('f').put('controller', Js([Js('$scope'), Js('$modalInstance'), PyJs_anonymous_50_])))),var.get('b').callprop('open', var.get('f')).get('result'))
    PyJs_anonymous_47_._set_name('anonymous')
    return PyJsComma(PyJsComma(var.get('e').put('showModal', PyJs_anonymous_45_),var.get('e').put('show', PyJs_anonymous_47_)),var.get('e'))
PyJs_anonymous_41_._set_name('anonymous')
PyJsComma(PyJs_LONG_40_().callprop('config', Js([Js('$locationProvider'), PyJs_anonymous_20_])).callprop('config', Js([Js('$routeProvider'), Js('$locationProvider'), PyJs_anonymous_0_])),var.get('angular').callprop('module', Js('tmcApp')).callprop('factory', Js('modalService'), Js([Js('$http'), Js('$modal'), PyJs_anonymous_41_])))
PyJs_Object_53_ = Js({})
var.put('NEB', (var.get('NEB') or PyJs_Object_53_))
@Js
def PyJs_anonymous_54_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['b', 'a'])
    var.put('a', var.get('a').callprop('replace', JsRegExp('/^\\s+/'), Js('')))
    #for JS loop
    var.put('b', (var.get('a').get('length')-Js(1.0)))
    while (var.get('b')>=Js(0.0)):
        try:
            if JsRegExp('/\\S/').callprop('test', var.get('a').callprop('charAt', var.get('b'))):
                var.put('a', var.get('a').callprop('substring', Js(0.0), (var.get('b')+Js(1.0))))
                break
        finally:
                (var.put('b',Js(var.get('b').to_number())-Js(1))+Js(1))
    return var.get('a')
PyJs_anonymous_54_._set_name('anonymous')
@Js
def PyJs_anonymous_55_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['c', 'f', 'b', 'd', 'a', 'e'])
    var.put('d', Js('ACGTUKMSWRYBDHVNacgtukmswrybdhvn'))
    var.put('e', Js('TGCAAMKWSYRVHDBNtgcaamkwsyrvhdbn'))
    var.put('f', var.get('a').callprop('split', Js('')).callprop('reverse'))
    #for JS loop
    var.put('b', Js(0.0))
    while (var.get('b')<var.get('f').get('length')):
        try:
            if PyJsComma(var.put('c', var.get('d').callprop('indexOf', var.get('f').get(var.get('b')))),PyJsStrictEq((-Js(1.0)),var.get('c'))):
                PyJs_Object_56_ = Js({'name':Js('InvalidCharacter'),'message':Js('A non IUPAC base was encountered')})
                PyJsTempException = JsToPyException(PyJs_Object_56_)
                raise PyJsTempException
            var.get('f').put(var.get('b'), var.get('e').callprop('charAt', var.get('c')))
        finally:
                var.put('b',Js(var.get('b').to_number())+Js(1))
    return var.get('f').callprop('join', Js(''))
PyJs_anonymous_55_._set_name('anonymous')
@Js
def PyJs_anonymous_57_(a, b, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['c', 'f', 'b', 'd', 'a', 'e'])
    var.put('c', Js(' acgt'))
    var.put('c', var.get('c').callprop('toUpperCase'), '+')
    var.put('d', Js(' acgtwsrymkbdhvn'))
    var.put('d', var.get('d').callprop('toUpperCase'), '+')
    pass
    #for JS loop
    PyJsComma(var.put('e', (var.get('c') if PyJsStrictEq(var.get('b'),Js(1.0).neg()) else var.get('d'))),var.put('f', Js(0.0)))
    while (var.get('f')<var.get('a').get('length')):
        try:
            if PyJsStrictEq((-Js(1.0)),var.get('e').callprop('indexOf', var.get('a').callprop('charAt', var.get('f')))):
                return Js(1.0).neg()
        finally:
                var.put('f',Js(var.get('f').to_number())+Js(1))
    return Js(0.0).neg()
PyJs_anonymous_57_._set_name('anonymous')
@Js
def PyJs_anonymous_58_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['b', 'a'])
    pass
    return PyJsComma(var.put('b', (var.get('a')/Js(1.0))),var.get('isNaN')(var.get('b')).neg())
PyJs_anonymous_58_._set_name('anonymous')
@Js
def PyJs_anonymous_59_(a, this, arguments, var=var):
    var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a'])
    (((Js('undefined')!=var.get('console',throw=False).typeof()) and (Js('function')==var.get('console').get('log').typeof())) and var.get('console').callprop('log', var.get('a')))
PyJs_anonymous_59_._set_name('anonymous')
PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('NEB').put('trim', PyJs_anonymous_54_),var.get('NEB').put('revcomp', PyJs_anonymous_55_)),var.get('NEB').put('isValidSeq', PyJs_anonymous_57_)),var.get('NEB').put('isNumeric', PyJs_anonymous_58_)),var.get('NEB').put('dmsg', PyJs_anonymous_59_))
PyJs_Object_60_ = Js({})
var.put('NEB', (var.get('NEB') or PyJs_Object_60_))
def PyJs_LONG_185_(var=var):
    @Js
    def PyJs_anonymous_61_(a, this, arguments, var=var):
        var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
        var.registers(['f', 'h', 'd', 'o', 'x', 'e', 'b', 'w', 't', 'a', 'r', 'i', 'm', 's', 'y', 'g', 'A', 'n', 'l', 'k', 'z', 'c', 'j', 'v', 'q', 'B', 'u', 'p'])
        var.put('b', var.get(u"null"))
        var.put('c', (var.get('a').get('ct') or Js(0.25)))
        var.put('d', (var.get('a').get('salt') or Js(50.0)))
        var.put('e', (var.get('a').get('dmso') or Js(0.0)))
        var.put('f', (var.get('a').get('methodid') or Js(4.0)))
        var.put('g', (Js(0.001)*var.get('d')))
        var.put('h', Js(1.987))
        PyJs_Object_62_ = Js({'aa':(-Js(24.0)),'tt':(-Js(24.0)),'at':(-Js(23.9)),'ta':(-Js(16.9)),'ca':(-Js(12.9)),'tg':(-Js(12.9)),'gt':(-Js(17.3)),'ac':(-Js(17.3)),'ct':(-Js(20.8)),'ag':(-Js(20.8)),'ga':(-Js(13.5)),'tc':(-Js(13.5)),'cg':(-Js(27.8)),'gc':(-Js(26.7)),'gg':(-Js(26.6)),'cc':(-Js(26.6))})
        var.put('i', PyJs_Object_62_)
        PyJs_Object_63_ = Js({'aa':(-Js(22.2)),'tt':(-Js(22.2)),'at':(-Js(20.4)),'ta':(-Js(21.3)),'ca':(-Js(22.7)),'tg':(-Js(22.7)),'gt':(-Js(22.4)),'ac':(-Js(22.4)),'ct':(-Js(21.0)),'ag':(-Js(21.0)),'ga':(-Js(22.2)),'tc':(-Js(22.2)),'cg':(-Js(27.2)),'gc':(-Js(24.4)),'gg':(-Js(19.9)),'cc':(-Js(19.9))})
        var.put('j', PyJs_Object_63_)
        PyJs_Object_64_ = Js({'aa':(-Js(9.1)),'tt':(-Js(9.1)),'at':(-Js(8.6)),'ta':(-Js(6.0)),'ca':(-Js(5.8)),'tg':(-Js(5.8)),'gt':(-Js(6.5)),'ac':(-Js(6.5)),'ct':(-Js(7.8)),'ag':(-Js(7.8)),'ga':(-Js(5.6)),'tc':(-Js(5.6)),'cg':(-Js(11.9)),'gc':(-Js(11.1)),'gg':(-Js(11.0)),'cc':(-Js(11.0))})
        var.put('k', PyJs_Object_64_)
        PyJs_Object_65_ = Js({'aa':(-Js(7.9)),'tt':(-Js(7.9)),'at':(-Js(7.2)),'ta':(-Js(7.2)),'ca':(-Js(8.5)),'tg':(-Js(8.5)),'gt':(-Js(8.4)),'ac':(-Js(8.4)),'ct':(-Js(7.8)),'ag':(-Js(7.8)),'ga':(-Js(8.2)),'tc':(-Js(8.2)),'cg':(-Js(10.6)),'gc':(-Js(9.8)),'gg':(-Js(8.0)),'cc':(-Js(8.0))})
        var.put('l', PyJs_Object_65_)
        var.put('m', Js(0.0).neg())
        var.put('n', Js(0.0))
        var.put('o', var.get(u"null"))
        var.put('p', var.get(u"null"))
        var.put('q', Js(0.0))
        var.put('r', Js(0.0))
        var.put('s', Js(0.0))
        var.put('t', Js(0.0))
        var.put('u', Js(0.0))
        @Js
        def PyJs_anonymous_66_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            def PyJs_LONG_67_(var=var):
                return PyJsComma(PyJsComma(var.get(u"this").put('sc_sch', ((Js(16.6)*var.get('Math').callprop('log', var.get(u"this").get('saltc')))/var.get('Math').get('LN10'))),var.get(u"this").put('sc_sl', ((Js(0.368)*var.get(u"this").get('wseq').get('length'))*var.get('Math').callprop('log', var.get(u"this").get('saltc'))))),var.get(u"this").put('sc_ow', (((Js(1e-05)*((Js(4.29)*var.get(u"this").get('fgc'))-Js(3.95)))*var.get('Math').callprop('log', var.get(u"this").get('saltc')))+((Js(9.4e-06)*var.get('Math').callprop('log', var.get(u"this").get('saltc')))*var.get('Math').callprop('log', var.get(u"this").get('saltc'))))))
            PyJs_LONG_67_()
        PyJs_anonymous_66_._set_name('anonymous')
        var.put('v', PyJs_anonymous_66_)
        @Js
        def PyJs_anonymous_68_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return PyJsComma(var.get(u"this").put('method', var.get('a')),var.get(u"this"))
        PyJs_anonymous_68_._set_name('anonymous')
        var.put('w', PyJs_anonymous_68_)
        @Js
        def PyJs_anonymous_69_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['b', 'a'])
            pass
            if var.get('a').neg():
                PyJs_Object_70_ = Js({'name':Js('Missing seq'),'message':Js('setSeq: no sequence provided')})
                PyJsTempException = JsToPyException(PyJs_Object_70_)
                raise PyJsTempException
            #for JS loop
            def PyJs_LONG_71_(var=var):
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get(u"this").put('seq', var.get('a')),var.get(u"this").put('wseq', var.get('NEB').callprop('trim', var.get(u"this").get('seq').callprop('toLowerCase').callprop('replace', Js(' '), Js(''))))),var.get(u"this").put('cseq', var.get('NEB').callprop('revcomp', var.get(u"this").get('wseq')))),var.get(u"this").put('sym', (Js(0.0).neg() if PyJsStrictEq(var.get(u"this").get('wseq'),var.get(u"this").get('cseq')) else Js(1.0).neg()))),var.get(u"this").put('primerc', (Js(1e-06)*var.get(u"this").get('ct')))),var.get(u"this").put('gc_cnt', Js(0.0))),var.put('b', Js(0.0)))
            PyJs_LONG_71_()
            while (var.get('b')<var.get(u"this").get('wseq').get('length')):
                try:
                    ((PyJsStrictEq(Js('g'),var.get(u"this").get('wseq').callprop('charAt', var.get('b'))) or PyJsStrictEq(Js('c'),var.get(u"this").get('wseq').callprop('charAt', var.get('b')))) and var.get(u"this").put('gc_cnt', Js(1.0), '+'))
                finally:
                        var.put('b',Js(var.get('b').to_number())+Js(1))
            return PyJsComma(PyJsComma(var.get(u"this").put('fgc', (var.get(u"this").get('gc_cnt')/var.get(u"this").get('wseq').get('length'))),var.get(u"this").callprop('saltCorrect')),var.get(u"this"))
        PyJs_anonymous_69_._set_name('anonymous')
        var.put('x', PyJs_anonymous_69_)
        @Js
        def PyJs_anonymous_72_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return PyJsComma(PyJsComma(var.get(u"this").put('ct', var.get('a')),var.get(u"this").put('primerc', (Js(1e-06)*var.get(u"this").get('ct')))),var.get(u"this"))
        PyJs_anonymous_72_._set_name('anonymous')
        var.put('y', PyJs_anonymous_72_)
        @Js
        def PyJs_anonymous_73_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return PyJsComma(PyJsComma(var.get(u"this").put('salt', var.get('a')),var.get(u"this").put('saltc', (Js(0.001)*var.get(u"this").get('salt')))),var.get(u"this"))
        PyJs_anonymous_73_._set_name('anonymous')
        var.put('z', PyJs_anonymous_73_)
        @Js
        def PyJs_anonymous_74_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return PyJsComma(var.get(u"this").put('dmso', var.get('a')),var.get(u"this"))
        PyJs_anonymous_74_._set_name('anonymous')
        var.put('A', PyJs_anonymous_74_)
        @Js
        def PyJs_anonymous_75_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'j', 'i', 'f', 'h', 'b', 'd', 'g', 'a', 'e'])
            if (var.get('a').neg() or PyJsStrictEq(Js(''),var.get('a'))):
                PyJs_Object_76_ = Js({'name':Js('Missing seq'),'message':Js('calcTm: A sequence must be present to calculate Tm')})
                PyJsTempException = JsToPyException(PyJs_Object_76_)
                raise PyJsTempException
            PyJsComma(var.get(u"this").callprop('setSeq', var.get('a')),var.get(u"this").callprop('saltCorrect'))
            var.put('d', Js(0.0))
            var.put('e', Js(0.0))
            var.put('f', Js(0.0))
            var.put('g', Js(0.0))
            var.put('h', Js(0.0))
            var.put('i', Js(0.0))
            var.put('j', var.get(u"this").get('primerc'))
            while 1:
                SWITCHED = False
                CONDITION = (var.get(u"this").get('method'))
                if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
                    SWITCHED = True
                    #for JS loop
                    PyJsComma(var.put('g', ((-Js(12.4)) if var.get(u"this").get('sym') else (-Js(10.8))), '+'),var.put('b', Js(0.0)))
                    while (var.get('b')<(var.get(u"this").get('wseq').get('length')-Js(1.0))):
                        try:
                            PyJsComma(PyJsComma(var.put('c', var.get(u"this").get('wseq').callprop('slice', var.get('b'), (var.get('b')+Js(2.0)))),var.put('e', var.get(u"this").get('dSBr').get(var.get('c')), '+')),var.put('f', var.get(u"this").get('dHBr').get(var.get('c')), '+'))
                        finally:
                                var.put('b',Js(var.get('b').to_number())+Js(1))
                    PyJsComma(PyJsComma(var.put('f', Js(1000.0), '*'),var.put('j', Js(4.0), '/')),var.put('d', (((var.get('f')/((var.get('g')+var.get('e'))+(var.get(u"this").get('R')*var.get('Math').callprop('log', var.get('j')))))-Js(273.15))+var.get(u"this").get('sc_sch'))))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js(4.0)):
                    SWITCHED = True
                    #for JS loop
                    def PyJs_LONG_77_(var=var):
                        return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('i', ((-Js(1.4)) if var.get(u"this").get('sym') else Js(0.0))),((PyJsStrictEq(Js('a'),var.get(u"this").get('wseq').callprop('charAt', Js(0.0))) or PyJsStrictEq(Js('t'),var.get(u"this").get('wseq').callprop('charAt', Js(0.0)))) and PyJsComma(var.put('g', Js(4.1), '+'),var.put('h', Js(2300.0), '+')))),((PyJsStrictEq(Js('a'),var.get(u"this").get('wseq').callprop('charAt', (var.get(u"this").get('wseq').get('length')-Js(1.0)))) or PyJsStrictEq(Js('t'),var.get(u"this").get('wseq').callprop('charAt', (var.get(u"this").get('wseq').get('length')-Js(1.0))))) and PyJsComma(var.put('g', Js(4.1), '+'),var.put('h', Js(2300.0), '+')))),((PyJsStrictEq(Js('g'),var.get(u"this").get('wseq').callprop('charAt', Js(0.0))) or PyJsStrictEq(Js('c'),var.get(u"this").get('wseq').callprop('charAt', Js(0.0)))) and PyJsComma(var.put('g', (-Js(2.8)), '+'),var.put('h', Js(100.0), '+')))),((PyJsStrictEq(Js('g'),var.get(u"this").get('wseq').callprop('charAt', (var.get(u"this").get('wseq').get('length')-Js(1.0)))) or PyJsStrictEq(Js('c'),var.get(u"this").get('wseq').callprop('charAt', (var.get(u"this").get('wseq').get('length')-Js(1.0))))) and PyJsComma(var.put('g', (-Js(2.8)), '+'),var.put('h', Js(100.0), '+')))),var.put('b', Js(0.0)))
                    PyJs_LONG_77_()
                    while (var.get('b')<(var.get(u"this").get('wseq').get('length')-Js(1.0))):
                        try:
                            PyJsComma(PyJsComma(var.put('c', var.get(u"this").get('wseq').callprop('slice', var.get('b'), (var.get('b')+Js(2.0)))),var.put('e', var.get(u"this").get('dSSa').get(var.get('c')), '+')),var.put('f', var.get(u"this").get('dHSa').get(var.get('c')), '+'))
                        finally:
                                (var.put('b',Js(var.get('b').to_number())+Js(1))-Js(1))
                    def PyJs_LONG_78_(var=var):
                        return PyJsComma(PyJsComma(PyJsComma(var.put('f', Js(1000.0), '*'),var.put('d', ((var.get('f')+var.get('h'))/(((var.get('g')+var.get('i'))+var.get('e'))+(var.get(u"this").get('R')*var.get('Math').callprop('log', var.get('j'))))))),(var.put('d', (Js(1.0)/((Js(1.0)/var.get('d'))+(var.get(u"this").get('sc_sl')/(var.get('f')+var.get('h')))))) if PyJsStrictEq(Js(3.0),var.get(u"this").get('method')) else (PyJsStrictEq(Js(4.0),var.get(u"this").get('method')) and var.put('d', (Js(1.0)/((Js(1.0)/var.get('d'))+var.get(u"this").get('sc_ow'))))))),var.put('d', Js(273.15), '-'))
                    PyJs_LONG_78_()
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js(7.0)):
                    SWITCHED = True
                    var.put('d', (((Js(81.5)+((Js(16.6)*var.get('Math').callprop('log', var.get(u"this").get('saltc')))/var.get('Math').get('LN10')))+(Js(0.41)*var.get(u"this").get('fgc')))-(Js(675.0)/var.get(u"this").get('wseq').get('length'))))
                SWITCHED = True
                break
            PyJs_Object_79_ = Js({'method':var.get(u"this").get('method'),'wseq':var.get(u"this").get('wseq'),'tm':var.get('d'),'dh':var.get('f'),'ds':var.get('e'),'salt':var.get(u"this").get('saltc'),'ct':var.get(u"this").get('primerc'),'dmso':var.get(u"this").get('dmso'),'fgc':var.get(u"this").get('fgc'),'len':var.get(u"this").get('wseq').get('length')})
            return PyJsComma(var.put('d', (Js(0.6)*var.get(u"this").get('dmso')), '-'),PyJs_Object_79_)
        PyJs_anonymous_75_._set_name('anonymous')
        var.put('B', PyJs_anonymous_75_)
        PyJs_Object_80_ = Js({'setSeq':var.get('x'),'setSalt':var.get('z'),'setCt':var.get('y'),'setDMSO':var.get('A'),'setMethod':var.get('w'),'saltCorrect':var.get('v'),'Tm':var.get('B'),'gc_cnt':var.get('q'),'fgc':var.get('r'),'sc_sch':var.get('s'),'sc_sl':var.get('t'),'sc_ow':var.get('u'),'seq':var.get('b'),'ct':var.get('c'),'salt':var.get('d'),'dmso':var.get('e'),'method':var.get('f'),'wseq':var.get('o'),'cseq':var.get('p'),'sym':var.get('m'),'primerc':var.get('n'),'saltc':var.get('g'),'R':var.get('h'),'dSSa':var.get('j'),'dHSa':var.get('l'),'dSBr':var.get('i'),'dHBr':var.get('k')})
        return PyJs_Object_80_
    PyJs_anonymous_61_._set_name('anonymous')
    @Js
    def PyJs_anonymous_81_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['a'])
        PyJs_Object_82_ = Js({})
        var.put('a', var.get('NEB').callprop('createTmCalc', PyJs_Object_82_))
        return var.get('a')
    PyJs_anonymous_81_._set_name('anonymous')
    @Js
    def PyJs_anonymous_83_(a, this, arguments, var=var):
        var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'b', 'd', 'a', 'e'])
        var.put('b', var.get(u"null"))
        var.put('c', Js('tmcdata/tmcalculatordata.json'))
        @Js
        def PyJs_anonymous_84_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            var.put('b', var.get('a').get('data'))
        PyJs_anonymous_84_._set_name('anonymous')
        var.put('d', var.get('a').callprop('get', var.get('c')).callprop('then', PyJs_anonymous_84_))
        PyJs_Object_86_ = Js({})
        @Js
        def PyJs_anonymous_87_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get('b')
        PyJs_anonymous_87_._set_name('anonymous')
        @Js
        def PyJs_anonymous_88_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get('b').get('groups')
        PyJs_anonymous_88_._set_name('anonymous')
        @Js
        def PyJs_anonymous_89_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'a'])
            var.put('c', Js([]))
            for PyJsTemp in var.get('b').get('groups'):
                var.put('a', PyJsTemp)
                (var.get('b').get('groups').callprop('hasOwnProperty', var.get('a')) and var.get('c').callprop('push', var.get('a')))
            return var.get('c')
        PyJs_anonymous_89_._set_name('anonymous')
        @Js
        def PyJs_anonymous_90_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get('b').get('prods')
        PyJs_anonymous_90_._set_name('anonymous')
        @Js
        def PyJs_anonymous_91_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get('b').get('buffs')
        PyJs_anonymous_91_._set_name('anonymous')
        @Js
        def PyJs_anonymous_92_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return var.get('b').get('buffs').get(var.get('b').get('prods').get(var.get('a')).get('buffer'))
        PyJs_anonymous_92_._set_name('anonymous')
        @Js
        def PyJs_anonymous_93_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return var.get('b').get('prods').get(var.get('a')).get('buffer')
        PyJs_anonymous_93_._set_name('anonymous')
        @Js
        def PyJs_anonymous_94_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'f', 'd', 'a', 'e'])
            #for JS loop
            var.put('d', var.get('b').get('groups').get(var.get('a')))
            var.put('e', Js([]))
            var.put('f', Js(0.0))
            while (var.get('f')<var.get('d').get('length')):
                try:
                    PyJsComma(PyJsComma(var.put('c', var.get('b').get('prods').get(var.get('d').get(var.get('f')))),var.get('c').put('id', var.get('d').get(var.get('f')))),var.get('e').callprop('push', var.get('c')))
                finally:
                        var.put('f',Js(var.get('f').to_number())+Js(1))
            return var.get('e')
        PyJs_anonymous_94_._set_name('anonymous')
        @Js
        def PyJs_anonymous_95_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'a', 'd', 'e'])
            var.put('d', Js([]))
            var.put('e', var.get('b').get('groups').get(var.get('a')))
            for PyJsTemp in var.get('e'):
                var.put('c', PyJsTemp)
                var.get('d').callprop('push', var.get('b').get('prods').get(var.get('e').get(var.get('c'))).get('name'))
            return var.get('d')
        PyJs_anonymous_95_._set_name('anonymous')
        @Js
        def PyJs_anonymous_96_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            return var.get('b').get('prods').get(var.get('a'))
        PyJs_anonymous_96_._set_name('anonymous')
        @Js
        def PyJs_anonymous_97_(a, this, arguments, var=var):
            var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
            var.registers(['a'])
            var.get(u"this").put('saveddata', var.get('a'))
        PyJs_anonymous_97_._set_name('anonymous')
        @Js
        def PyJs_anonymous_98_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('savedata')
        PyJs_anonymous_98_._set_name('anonymous')
        @Js
        def PyJs_anonymous_99_(a, b, c, d, e, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'this':this, 'arguments':arguments}, var)
            var.registers(['j', 'l', 'i', 'm', 'f', 'h', 'b', 'c', 'd', 'o', 'g', 'a', 'n', 'k', 'e', 'p'])
            var.put('f', Js([]))
            var.put('g', Js(1.0).neg())
            var.put('h', Js([]))
            var.put('i', Js(1.0).neg())
            var.put('j', var.get('a').get('length'))
            var.put('k', var.get('b').get('length'))
            var.put('l', Js(0.0).neg())
            var.put('m', Js(0.0).neg())
            var.put('n', Js(0.0).neg())
            var.put('o', Js(''))
            var.put('p', Js(''))
            def PyJs_LONG_103_(var=var):
                def PyJs_LONG_100_(var=var):
                    return (var.get('h').callprop('push', Js('The recommended primer concentration for Phusion reactions is 500 nM.')) if ((Js(0.5)>var.get('c')) and PyJsStrictNeq((-Js(1.0)),var.get('e').callprop('indexOf', Js('Phusion')))) else (var.get('h').callprop('push', Js('The recommended primer concentration for LongAmp reactions is 400 nM.')) if ((Js(0.4)>var.get('c')) and PyJsStrictNeq((-Js(1.0)),var.get('e').callprop('indexOf', Js('LongAmp')))) else ((Js(0.2)>var.get('c')) and var.get('h').callprop('push', Js('The recommended primer concentration is 200 nM.')))))
                def PyJs_LONG_101_(var=var):
                    return (PyJsComma((var.get('m') or PyJsComma(PyJsComma(var.get('f').callprop('push', Js('Primer 1 has invalid bases. ')),var.put('g', Js(0.0).neg())),var.put('o', Js('invalidseq')))),(var.get('n') or PyJsComma(PyJsComma(var.get('f').callprop('push', Js('Primer 2 has invalid bases. ')),var.put('g', Js(0.0).neg())),var.put('p', Js('invalidseq'))))) if (var.get('m') or var.get('n')) else PyJsComma(PyJsComma(PyJsComma(var.get('f').callprop('push', Js('Both primers have invalid bases. ')),var.put('g', Js(0.0).neg())),var.put('o', Js('invalidseq'))),var.put('p', Js('invalidseq'))))
                PyJs_Object_102_ = Js({'hasWarnings':var.get('i'),'warnings':var.get('h'),'hasCritWarnings':var.get('g'),'critwarnings':var.get('f'),'ctisValid':var.get('l'),'p1isValid':var.get('m'),'p2isValid':var.get('n'),'p1status':var.get('o'),'p2status':var.get('p')})
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma((((Js(0.0)>=var.get('c')) or var.get('isNaN')((var.get('c')/Js(1.0)))) and PyJsComma(PyJsComma(var.put('l', Js(1.0).neg()),var.put('g', Js(0.0).neg())),var.get('f').callprop('push', Js('Invalid primer concentration. ')))),PyJs_LONG_100_()),var.put('m', var.get('NEB').callprop('isValidSeq', var.get('a'), Js(1.0).neg()))),var.put('n', var.get('NEB').callprop('isValidSeq', var.get('b'), Js(1.0).neg()))),PyJs_LONG_101_()),(PyJsStrictEq(Js(0.0),var.get('j')) and PyJsComma(PyJsComma(var.get('f').callprop('push', Js('Primer 1 missing. ')),var.put('g', Js(0.0).neg())),var.put('o', Js('invalidseq'))))),(PyJsStrictEq(Js(0.0),var.get('k')) and PyJsComma(PyJsComma(var.get('f').callprop('push', Js('Primer 2 missing. ')),var.put('g', Js(0.0).neg())),var.put('p', Js('invalidseq'))))),(((Js(8.0)>var.get('j')) or (Js(8.0)>var.get('k'))) and PyJsComma(PyJsComma((((var.get('j')>Js(0.0)) or (var.get('k')>Js(0.0))) and PyJsComma(var.get('f').callprop('push', Js('Both primers need to be longer than 7 nt')),var.put('g', Js(0.0).neg()))),((Js(8.0)>var.get('j')) and var.put('o', Js('invalidseq')))),((Js(8.0)>var.get('k')) and var.put('p', Js('invalidseq')))))),PyJs_Object_102_)
            return PyJs_LONG_103_()
        PyJs_anonymous_99_._set_name('anonymous')
        @Js
        def PyJs_anonymous_104_(a, b, c, d, e, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'f', 'b', 'd', 'g', 'a', 'e'])
            var.put('f', Js([]))
            var.put('g', Js([]))
            def PyJs_LONG_105_(var=var):
                return (var.get('g').callprop('push', Js(' Annealing temperature is lower than the recommended minimum of 50 °C.')) if ((PyJsStrictNeq(Js(''),var.get('c')) and (Js(50.0)>var.get('c'))) and PyJsStrictNeq((-Js(1.0)),var.get('e').callprop('indexOf', Js('Q5')))) else ((PyJsStrictNeq(Js(''),var.get('c')) and (Js(45.0)>var.get('c'))) and var.get('g').callprop('push', Js(' Annealing temperature is lower than the recommended minimum of 45 °C.'))))
            def PyJs_LONG_107_(var=var):
                def PyJs_LONG_106_(var=var):
                    return (((var.get('c')>=Js(65.0)) and var.get('f').callprop('push', Js('Annealing temperature for experiments with this enzyme should typically not exceed 65°C.'))) if (PyJsStrictEq(Js('LongAmp Taq'),var.get('e')) or PyJsStrictEq(Js('LongAmp Hot Start Taq'),var.get('e'))) else ((var.get('c')>=Js(68.0)) and var.get('f').callprop('push', Js('Annealing temperature for experiments with this enzyme should typically not exceed 68°C.'))))
                return (((var.get('c')>=Js(72.0)) and var.get('f').callprop('push', Js('Annealing temperature for experiments with this enzyme should typically not exceed 72°C.'))) if ((((PyJsStrictEq(Js('Phusion'),var.get('e')) or PyJsStrictEq(Js('Vent'),var.get('e'))) or PyJsStrictEq(Js('Deep Vent'),var.get('e'))) or PyJsStrictEq(Js('Phusion Flex'),var.get('e'))) or PyJsStrictNeq((-Js(1.0)),var.get('e').callprop('indexOf', Js('Q5')))) else PyJs_LONG_106_())
            PyJs_Object_108_ = Js({'hasWarnings':(var.get('f').get('length')>Js(0.0)),'warnings':var.get('f'),'hasCritWarnings':(var.get('g').get('length')>Js(0.0)),'critwarnings':var.get('g')})
            return PyJsComma(PyJsComma(PyJsComma(((((var.get('a')-var.get('b'))*(var.get('a')-var.get('b')))>Js(25.0)) and var.get('g').callprop('push', Js('Tm difference is greater than the recommended limit of 5 °C. '))),PyJs_LONG_105_()),(((PyJsStrictNeq(Js(''),var.get('c')) and (var.get('c')>=Js(65.0))) and ((var.get('a')>var.get('c')) or (var.get('b')>var.get('c')))) and PyJs_LONG_107_())),PyJs_Object_108_)
        PyJs_anonymous_104_._set_name('anonymous')
        @Js
        def PyJs_anonymous_109_(a, b, c, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'b', 'd', 'a', 'e'])
            var.put('d', Js([]))
            var.put('e', Js([]))
            def PyJs_LONG_110_(var=var):
                return (var.get('d').callprop('push', Js('DMSO can improve PCR amplification from GC-rich templates,  but it is also known to reduce the annealing temperature of primers in a PCR reaction. Therefore,  it is recommended that for every 1% of additional DMSO added, the calculated annealing temperature should be reduced by 0.6°C [Chester and Marshak,  1993. Analytical Biochemistry 209,  284-290].')) if ((PyJsStrictEq(Js('phusion_gc'),var.get('c')) or PyJsStrictEq(Js('onetaq_gc'),var.get('c'))) or PyJsStrictEq(Js('phusionflex_gc'),var.get('c'))) else (PyJsStrictEq(Js('q5'),var.get('c')) and var.get('d').callprop('push', Js('Use of the Q5 High GC Enhancer often lowers the range of temperatures at which specific amplification can be observed, however the rule used to determine Q5 annealing temperatures (Ta = Tm_lower+1°C) typically yields values that will support specific amplification with or without the enhancer.'))))
            PyJs_Object_111_ = Js({'hasWarnings':(var.get('d').get('length')>Js(0.0)),'warnings':var.get('d'),'hasCritWarnings':(var.get('e').get('length')>Js(0.0)),'critwarnings':var.get('e')})
            return PyJsComma(PyJs_LONG_110_(),PyJs_Object_111_)
        PyJs_anonymous_109_._set_name('anonymous')
        @Js
        def PyJs_anonymous_112_(a, b, c, d, e, f, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'f':f, 'this':this, 'arguments':arguments}, var)
            var.registers(['j', 'c', 'i', 'f', 'h', 'b', 'd', 'g', 'a', 'k', 'e'])
            var.put('j', var.get('a').callprop('replace', JsRegExp('/\\s/g'), Js('')).get('length'))
            var.put('k', var.get('c').callprop('replace', JsRegExp('/\\s/g'), Js('')).get('length'))
            while 1:
                SWITCHED = False
                CONDITION = (PyJsComma(PyJsComma(PyJsComma(var.put('h', (var.get('b') if (var.get('d')>var.get('b')) else var.get('d'))),var.put('i', (var.get('j') if (var.get('k')>var.get('j')) else var.get('k')))),var.put('g', var.get('h'))),var.get('e')))
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Taq DNA Polymerase')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Hemo KlenTaq')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('OneTaq')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('OneTaq Hot Start')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('EpiMark Hot Start')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Hot Start Taq')):
                    SWITCHED = True
                    PyJsComma(((var.get('i')>Js(7.0)) and var.put('g', (var.get('h')-Js(5.0)))),((var.get('g')>Js(68.0)) and var.put('g', Js(68.0))))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('LongAmp Taq')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('LongAmp Hot Start Taq')):
                    SWITCHED = True
                    PyJsComma(((var.get('i')>Js(7.0)) and var.put('g', (var.get('h')-Js(5.0)))),((var.get('g')>Js(65.0)) and var.put('g', Js(65.0))))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Vent')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Deep Vent')):
                    SWITCHED = True
                    PyJsComma(((var.get('i')>Js(20.0)) and var.put('g', (var.get('h')-Js(2.0)))),((var.get('g')>Js(72.0)) and var.put('g', Js(72.0))))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Phusion')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Phusion Hot Start Flex')):
                    SWITCHED = True
                    PyJsComma(((var.get('i')>Js(20.0)) and var.put('g', (var.get('h')+Js(3.0)))),((var.get('g')>Js(72.0)) and var.put('g', Js(72.0))))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Q5')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Q5 Hot Start')):
                    SWITCHED = True
                    PyJsComma(((var.get('i')>Js(7.0)) and var.put('g', (var.get('h')+Js(1.0)))),((var.get('g')>Js(72.0)) and var.put('g', Js(72.0))))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Master Mix')):
                    SWITCHED = True
                    def PyJs_LONG_114_(var=var):
                        def PyJs_LONG_113_(var=var):
                            return (PyJsComma(((var.get('i')>Js(20.0)) and var.put('g', (var.get('h')-Js(2.0)))),((var.get('g')>Js(72.0)) and var.put('g', Js(72.0)))) if (PyJsStrictEq(Js(0.0),var.get('f').callprop('indexOf', Js('vent'))) or PyJsStrictEq(Js(0.0),var.get('f').callprop('indexOf', Js('deepvent')))) else PyJsComma(((var.get('i')>Js(7.0)) and var.put('g', (var.get('h')-Js(5.0)))),((var.get('g')>Js(68.0)) and var.put('g', Js(68.0)))))
                        return (PyJsComma(((var.get('i')>Js(7.0)) and var.put('g', (var.get('h')+Js(1.0)))),((var.get('g')>Js(72.0)) and var.put('g', Js(72.0)))) if PyJsStrictEq(Js(0.0),var.get('f').callprop('indexOf', Js('q5'))) else (PyJsComma(((var.get('i')>Js(20.0)) and var.put('g', (var.get('h')+Js(3.0)))),((var.get('g')>Js(72.0)) and var.put('g', Js(72.0)))) if PyJsStrictEq(Js(0.0),var.get('f').callprop('indexOf', Js('phusion'))) else PyJs_LONG_113_()))
                    PyJs_LONG_114_()
                    break
                if True:
                    SWITCHED = True
                    var.put('g', var.get('h'))
                SWITCHED = True
                break
            return (var.get('Math').callprop('round', (Js(10.0)*var.get('g')))/Js(10.0))
        PyJs_anonymous_112_._set_name('anonymous')
        PyJs_Object_85_ = Js({'saveddata':PyJs_Object_86_,'promise':var.get('d'),'tmcdata':var.get('b'),'getData':PyJs_anonymous_87_,'getGroups':PyJs_anonymous_88_,'getGroupKeys':PyJs_anonymous_89_,'getProducts':PyJs_anonymous_90_,'getBuffers':PyJs_anonymous_91_,'getBufferSaltForProduct':PyJs_anonymous_92_,'getBufferIdForProduct':PyJs_anonymous_93_,'getProductsForGroup':PyJs_anonymous_94_,'getProductKeysForGroup':PyJs_anonymous_95_,'getPropsForProduct':PyJs_anonymous_96_,'saveUserPrefs':PyJs_anonymous_97_,'restoreUserPrefs':PyJs_anonymous_98_,'validateInput':PyJs_anonymous_99_,'validateTm':PyJs_anonymous_104_,'validateBuffer':PyJs_anonymous_109_,'getAnnealTemp':PyJs_anonymous_112_})
        var.put('e', PyJs_Object_85_)
        return var.get('e')
    PyJs_anonymous_83_._set_name('anonymous')
    @Js
    def PyJs_anonymous_115_(a, b, c, d, e, this, arguments, var=var):
        var = Scope({'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'f', 'h', 'b', 'd', 'g', 'a', 'e'])
        def PyJs_LONG_119_(var=var):
            PyJs_Object_116_ = Js({})
            PyJs_Object_117_ = Js({})
            PyJs_Object_118_ = Js({})
            return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').put('input', PyJs_Object_116_),var.get('a').put('result', PyJs_Object_117_)),var.get('a').get('input').put('p1', Js(''))),var.get('a').get('input').put('p2', Js(''))),var.get('a').get('input').put('ct', Js(0.25))),var.get('a').get('result').put('tm1', var.get(u"null"))),var.get('a').get('result').put('tm2', var.get(u"null"))),var.get('a').get('result').put('len1', Js('---'))),var.get('a').get('result').put('len2', Js('---'))),var.get('a').get('result').put('gc1', Js('---'))),var.get('a').get('result').put('gc2', Js('---'))),var.get('a').get('result').put('ta', Js('---'))),var.get('a').get('result').put('itemlist', Js([]))),var.get('a').get('result').put('critlist', Js([]))),var.get('a').get('input').put('groupKeys', Js([]))),var.get('a').get('input').put('products', PyJs_Object_118_)),var.get('a').get('input').put('prodKeys', Js([]))),var.get('a').get('input').put('group', Js(''))),var.get('a').get('input').put('product', Js(''))),var.get('a').put('p1status', Js(''))),var.get('a').put('p2status', Js(''))),(PyJsComma(var.get('a').put('lastp1', var.get('b').callprop('restoreUserPrefs').get('p1')),var.get('a').put('lastp2', var.get('b').callprop('restoreUserPrefs').get('p2'))) if var.get('b').callprop('restoreUserPrefs') else PyJsComma(var.get('a').put('lastp1', Js('')),var.get('a').put('lastp2', Js('')))))
        PyJs_LONG_119_()
        var.put('f', ((var.get('d').get('p1seq') or var.get('a').get('lastp1')) or Js('')))
        var.put('g', ((var.get('d').get('p2seq') or var.get('a').get('lastp2')) or Js('')))
        @Js
        def PyJs_anonymous_120_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            PyJsComma(PyJsComma(var.get('a').get('input').put('p1', Js('AGCGGATAACAATTTCACACAGGA')),var.get('a').get('input').put('p2', Js('GTA AAA CGA CGG CCA GT'))),var.get('a').callprop('runCalc2'))
        PyJs_anonymous_120_._set_name('anonymous')
        @Js
        def PyJs_anonymous_121_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            def PyJs_LONG_122_(var=var):
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').get('input').put('p1', Js('')),var.get('a').get('input').put('p2', Js(''))),var.get('a').get('result').put('tm1', var.get(u"null"))),var.get('a').get('result').put('tm2', var.get(u"null"))),var.get('a').get('result').put('len1', Js('---'))),var.get('a').get('result').put('len2', Js('---'))),var.get('a').get('result').put('gc1', Js('---'))),var.get('a').get('result').put('gc2', Js('---'))),var.get('a').get('result').put('ta', Js('---'))),var.get('a').get('result').put('itemlist', Js([]))),var.get('a').get('result').put('critlist', Js([]))),var.get('a').put('p1status', Js(''))),var.get('a').put('p2status', Js('')))
            PyJs_LONG_122_()
        PyJs_anonymous_121_._set_name('anonymous')
        @Js
        def PyJs_anonymous_123_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            PyJsComma(var.get('a').get('input').put('groupKeys', var.get('b').callprop('getGroupKeys')),var.get('a').get('input').put('group', var.get('a').get('input').get('groupKeys').get('0')))
        PyJs_anonymous_123_._set_name('anonymous')
        @Js
        def PyJs_anonymous_124_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'd'])
            pass
            def PyJs_LONG_125_(var=var):
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('c', var.get('a').get('input').get('group')),var.get('a').get('input').put('productKeys', var.get('b').callprop('getProductKeysForGroup', var.get('c')))),var.get('a').get('input').put('products', var.get('b').callprop('getProductsForGroup', var.get('c')))),var.get('a').get('input').put('product', var.get('a').get('input').get('products').get('0').get('id'))),var.put('d', var.get('a').get('input').get('product'))),var.get('a').callprop('setCt'))
            PyJs_LONG_125_()
        PyJs_anonymous_124_._set_name('anonymous')
        @Js
        def PyJs_anonymous_126_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['b', 'c'])
            var.put('b', var.get('a').get('input').get('group'))
            var.put('c', var.get('a').get('input').get('product'))
            def PyJs_LONG_128_(var=var):
                def PyJs_LONG_127_(var=var):
                    return (var.get('a').get('input').put('ct', Js(500.0)) if (PyJsStrictEq(Js(0.0),var.get('c').callprop('indexOf', Js('phusion'))) or PyJsStrictEq(Js(0.0),var.get('c').callprop('indexOf', Js('q5')))) else (var.get('a').get('input').put('ct', Js(400.0)) if (PyJsStrictEq(Js(0.0),var.get('c').callprop('indexOf', Js('lataq'))) or PyJsStrictEq(Js(0.0),var.get('c').callprop('indexOf', Js('lahstaq')))) else var.get('a').get('input').put('ct', Js(200.0))))
                return (var.get('a').get('input').put('ct', Js(500.0)) if (PyJsStrictEq(Js(0.0),var.get('b').callprop('indexOf', Js('Phusion'))) or PyJsStrictEq(Js(0.0),var.get('b').callprop('indexOf', Js('Q5')))) else (var.get('a').get('input').put('ct', Js(400.0)) if PyJsStrictEq(Js(0.0),var.get('b').callprop('indexOf', Js('LongAmp'))) else (PyJs_LONG_127_() if PyJsStrictEq(Js(0.0),var.get('b').callprop('indexOf', Js('Master'))) else var.get('a').get('input').put('ct', Js(200.0)))))
            PyJsComma(PyJs_LONG_128_(),var.get('a').callprop('runCalc2'))
        PyJs_anonymous_126_._set_name('anonymous')
        @Js
        def PyJs_anonymous_129_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['f', 'h', 'd', 'o', 'x', 'e', 'w', 't', 'r', 'i', 'm', 's', 'y', 'g', 'A', 'n', 'l', 'k', 'z', 'j', 'v', 'q', 'u', 'p'])
            var.put('n', var.get('a').get('input').get('p1'))
            var.put('o', var.get('a').get('input').get('p2'))
            var.put('p', (var.get('a').get('input').get('ct')/Js(1000.0)))
            var.put('q', var.get('a').get('input').get('product'))
            var.put('r', var.get('a').get('input').get('group'))
            var.put('s', var.get('NEB').callprop('isNumeric', var.get('p')))
            var.put('t', Js([]))
            var.put('u', Js([]))
            var.put('v', Js(0.0))
            var.put('w', var.get('NEB').callprop('isValidSeq', var.get('n'), Js(1.0).neg()))
            var.put('x', var.get('NEB').callprop('isValidSeq', var.get('o'), Js(1.0).neg()))
            var.put('y', var.get('b').callprop('validateInput', var.get('n').callprop('replace', JsRegExp('/\\s/g'), Js('')), var.get('o').callprop('replace', JsRegExp('/\\s/g'), Js('')), var.get('p'), var.get('q'), var.get('r')))
            def PyJs_LONG_130_(var=var):
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('s', var.get('y').get('ctisValid')),var.put('w', var.get('y').get('p1isValid'))),var.put('x', var.get('y').get('p2isValid'))),var.put('h', var.get('y').get('hasCritWarnings'))),var.put('g', var.get('y').get('hasWarnings'))),var.put('u', var.get('y').get('critwarnings'))),var.put('t', var.get('y').get('warnings'))),var.get('a').put('p1status', var.get('y').get('p1status'))),var.get('a').put('p2status', var.get('y').get('p2status'))),var.get('a').get('result').put('itemlist', var.get('t'))),var.get('a').get('result').put('critlist', var.get('u'))),var.get('a').put('ctstatus', Js(''))),var.get('s').neg())
            if PyJs_LONG_130_():
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').get('result').put('ta', Js('---')),var.get('a').get('result').put('tm1', var.get(u"null"))),var.get('a').get('result').put('tm2', var.get(u"null"))),var.get('a').put('ctstatus', Js('invalidct'))),(var.get('w') and var.get('a').put('p1status', Js('')))),PyJsComma((var.get('x') and var.get('a').put('p2status', Js(''))), Js(None)))
            if (PyJsStrictEq(Js('invalidseq'),var.get('a').get('p1status')) and PyJsStrictEq(Js('invalidseq'),var.get('a').get('p2status'))):
                def PyJs_LONG_131_(var=var):
                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').get('result').put('tm1', var.get(u"null")),var.get('a').get('result').put('tm2', var.get(u"null"))),var.get('a').get('result').put('len1', Js('---'))),var.get('a').get('result').put('len2', Js('---'))),var.get('a').get('result').put('gc1', Js('---'))),var.get('a').get('result').put('gc2', Js('---'))),var.get('a').get('result').put('ta', Js('---'))),(var.get('w') and var.get('a').put('p1status', Js('')))),PyJsComma((var.get('x') and var.get('a').put('p2status', Js(''))), Js(None)))
                return PyJs_LONG_131_()
            while 1:
                SWITCHED = False
                def PyJs_LONG_132_(var=var):
                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma((PyJsStrictEq(Js('invalidseq'),var.get('a').get('p1status')) and PyJsComma(PyJsComma(PyJsComma(var.get('a').get('result').put('tm1', var.get(u"null")),var.get('a').get('result').put('len1', Js('---'))),var.get('a').get('result').put('gc1', Js('---'))),var.get('a').get('result').put('ta', Js('---')))),(PyJsStrictEq(Js('invalidseq'),var.get('a').get('p2status')) and PyJsComma(PyJsComma(PyJsComma(var.get('a').get('result').put('tm2', var.get(u"null")),var.get('a').get('result').put('len2', Js('---'))),var.get('a').get('result').put('gc2', Js('---'))),var.get('a').get('result').put('ta', Js('---'))))),var.put('d', var.get('b').callprop('getBufferIdForProduct', var.get('q')))),(PyJsStrictEq(Js('onetaq_gc'),var.get('d')) and var.put('v', Js(5.0)))),var.put('e', var.get('b').callprop('getBufferSaltForProduct', var.get('a').get('input').get('product')))),var.get('r'))
                CONDITION = (PyJs_LONG_132_())
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Phusion')):
                    SWITCHED = True
                    pass
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Phusion Hot Start Flex')):
                    SWITCHED = True
                    var.put('f', Js(1.0))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('Master Mix')):
                    SWITCHED = True
                    var.put('f', (Js(1.0) if PyJsStrictEq(Js(0.0),var.get('q').callprop('indexOf', Js('phusion'))) else Js(4.0)))
                    break
                if True:
                    SWITCHED = True
                    var.put('f', Js(4.0))
                SWITCHED = True
                break
            def PyJs_LONG_133_(var=var):
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('l', var.get('c').callprop('setCt', var.get('p')).callprop('setSalt', var.get('e')).callprop('setMethod', var.get('f')).callprop('setDMSO', var.get('v')).callprop('Tm', var.get('n').callprop('replace', JsRegExp('/\\s/g'), Js('')))),var.put('j', var.get('l').get('tm'))),var.put('j', var.get('Math').callprop('round', (var.get('Math').callprop('round', (Js(10.0)*var.get('j')))/Js(10.0))))),var.get('a').get('result').put('tm1', var.get('j'))),var.get('a').get('result').put('len1', var.get('l').get('len'))),var.get('a').get('result').put('gc1', (Js(100.0)*var.get('l').get('fgc')))),var.get('a').get('result').put('gc1', var.get('Math').callprop('round', ((Js(10.0)*var.get('a').get('result').get('gc1'))/Js(10.0)))))
            def PyJs_LONG_134_(var=var):
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('m', var.get('c').callprop('setCt', var.get('p')).callprop('setSalt', var.get('e')).callprop('setMethod', var.get('f')).callprop('setDMSO', var.get('v')).callprop('Tm', var.get('o').callprop('replace', JsRegExp('/\\s/g'), Js('')))),var.put('k', var.get('m').get('tm'))),var.put('k', var.get('Math').callprop('round', (var.get('Math').callprop('round', (Js(10.0)*var.get('k')))/Js(10.0))))),var.get('a').get('result').put('tm2', var.get('k'))),var.get('a').get('result').put('len2', var.get('m').get('len'))),var.get('a').get('result').put('gc2', (Js(100.0)*var.get('m').get('fgc')))),var.get('a').get('result').put('gc2', var.get('Math').callprop('round', ((Js(10.0)*var.get('a').get('result').get('gc2'))/Js(10.0)))))
            if PyJsComma(PyJsComma((PyJsStrictNeq(Js('invalidseq'),var.get('a').get('p1status')) and PyJs_LONG_133_()),(PyJsStrictNeq(Js('invalidseq'),var.get('a').get('p2status')) and PyJs_LONG_134_())),(PyJsStrictEq(Js('invalidseq'),var.get('a').get('p1status')) or PyJsStrictEq(Js('invalidseq'),var.get('a').get('p2status')))):
                return PyJsComma(var.get('a').get('result').put('ta', Js('---')), Js(None))
            PyJsComma(var.put('i', var.get('b').callprop('getAnnealTemp', var.get('n'), var.get('j'), var.get('o'), var.get('k'), var.get('r'), var.get('q'))),var.get('a').get('result').put('ta', var.get('Math').callprop('round', var.get('i'))))
            var.put('z', var.get('b').callprop('validateTm', var.get('j'), var.get('k'), var.get('i'), var.get('q'), var.get('r'), var.get('d')))
            var.put('A', var.get('b').callprop('validateBuffer', var.get('q'), var.get('r'), var.get('d')))
            def PyJs_LONG_135_(var=var):
                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('u', Js([])),var.put('t', Js([]))),(var.get('z').get('hasCritWarnings') and var.put('u', var.get('z').get('critwarnings')))),(var.get('z').get('hasWarnings') and var.put('t', var.get('z').get('warnings')))),(var.get('A').get('hasCritWarnings') and var.get('Array').get('prototype').get('push').callprop('apply', var.get('u'), var.get('A').get('critwarnings')))),(var.get('A').get('hasWarnings') and var.get('Array').get('prototype').get('push').callprop('apply', var.get('t'), var.get('A').get('warnings')))),var.get('a').get('result').put('itemlist', var.get('t'))),var.get('a').get('result').put('critlist', var.get('u')))
            PyJs_LONG_135_()
        PyJs_anonymous_129_._set_name('anonymous')
        PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').put('prefill', PyJs_anonymous_120_),var.get('a').put('clearCalc', PyJs_anonymous_121_)),var.get('a').put('setGroups', PyJs_anonymous_123_)),var.get('a').put('setProducts', PyJs_anonymous_124_)),var.get('a').put('setCt', PyJs_anonymous_126_)),var.get('a').put('runCalc2', PyJs_anonymous_129_))
        @Js
        def PyJs_anonymous_136_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return Js('Product selections and sequence data will not be preserved if you leave this page.')
        PyJs_anonymous_136_._set_name('anonymous')
        var.put('h', PyJs_anonymous_136_)
        def PyJs_LONG_140_(var=var):
            @Js
            def PyJs_anonymous_137_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('h')()
            PyJs_anonymous_137_._set_name('anonymous')
            @Js
            def PyJs_anonymous_138_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('e').callprop('path', Js('#/about'))
            PyJs_anonymous_138_._set_name('anonymous')
            @Js
            def PyJs_anonymous_139_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('e').callprop('path', Js('/batch'))
            PyJs_anonymous_139_._set_name('anonymous')
            return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').callprop('$on', Js('$routeChangeStart'), PyJs_anonymous_137_),var.get('a').put('about', PyJs_anonymous_138_)),var.get('a').put('switch2batch', PyJs_anonymous_139_)),var.get('a').get('input').put('p1', var.get('f'))),var.get('a').get('input').put('p2', var.get('g'))),var.get('a').callprop('setGroups')),var.get('a').callprop('setProducts')),var.get('a').callprop('clearCalc'))
        PyJs_LONG_140_()
    PyJs_anonymous_115_._set_name('anonymous')
    @Js
    def PyJs_anonymous_141_(a, this, arguments, var=var):
        var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
        var.registers(['a'])
        pass
    PyJs_anonymous_141_._set_name('anonymous')
    @Js
    def PyJs_anonymous_142_(a, b, c, d, e, f, this, arguments, var=var):
        var = Scope({'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'f':f, 'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'i', 'f', 'h', 'b', 'd', 'g', 'a', 'e'])
        def PyJs_LONG_146_(var=var):
            PyJs_Object_143_ = Js({})
            PyJs_Object_144_ = Js({})
            PyJs_Object_145_ = Js({})
            return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').put('input', PyJs_Object_143_),var.get('a').put('result', PyJs_Object_144_)),var.get('a').put('output', Js([]))),var.get('a').get('input').put('p1', Js(''))),var.get('a').get('input').put('p2', Js(''))),var.get('a').get('input').put('id1', Js(''))),var.get('a').get('input').put('id2', Js(''))),var.get('a').get('input').put('ct', Js(0.25))),var.get('a').get('result').put('tm1', Js(''))),var.get('a').get('result').put('tm2', Js(''))),var.get('a').get('result').put('ta', Js(''))),var.get('a').get('result').put('itemlist', Js([]))),var.get('a').get('result').put('critlist', Js([]))),var.get('a').get('input').put('groupKeys', Js([]))),var.get('a').get('input').put('products', PyJs_Object_145_)),var.get('a').get('input').put('prodKeys', Js([]))),var.get('a').get('input').put('group', Js(''))),var.get('a').get('input').put('product', Js(''))),var.get('a').get('input').put('batch', Js(''))),var.get('a').get('input').put('filename', Js(''))),var.get('a').get('result').put('batch', Js(''))),var.get('a').get('result').put('batch2', Js(''))),var.get('a').put('p1status', Js(''))),var.get('a').put('p2status', Js(''))),(PyJsComma(var.get('a').put('lastp1', var.get('b').callprop('restoreUserPrefs').get('p1')),var.get('a').put('lastp2', var.get('b').callprop('restoreUserPrefs').get('p2'))) if var.get('b').callprop('restoreUserPrefs') else PyJsComma(var.get('a').put('lastp1', Js('')),var.get('a').put('lastp2', Js('')))))
        PyJs_LONG_146_()
        var.put('g', ((var.get('d').get('p1seq') or var.get('a').get('lastp1')) or Js('')))
        var.put('h', ((var.get('d').get('p2seq') or var.get('a').get('lastp2')) or Js('')))
        def PyJs_LONG_167_(var=var):
            @Js
            def PyJs_anonymous_147_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                def PyJs_LONG_148_(var=var):
                    return PyJsComma(PyJsComma(PyJsComma(var.get('a').get('input').put('batch', Js('P1fwd\tAGCGGATAACAATTTCACACAGGA\tP1rev\tGTAAAACGACGGCCAGT\nP2fwd\tAGCGGATAACAATTTCAC\tP2rev\tGTAAAACGACGGCCA\n')),var.get('a').get('output').put('showresultstable', Js(1.0).neg())),var.get('a').put('data_toggle_label', (Js('Hide') if var.get('a').get('output').get('showresultstable') else Js('Show')))),var.get('a').callprop('runCalc3'))
                PyJs_LONG_148_()
            PyJs_anonymous_147_._set_name('anonymous')
            @Js
            def PyJs_anonymous_149_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['b'])
                def PyJs_LONG_150_(var=var):
                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').get('input').put('batch', Js('')),var.get('a').get('input').put('filename', Js(''))),var.get('a').put('output', Js([]))),var.get('a').get('result').put('itemlist', Js([]))),var.get('a').get('result').put('critlist', Js([]))),var.get('a').get('result').put('batch', Js(''))),var.get('a').get('result').put('batch2', Js(''))),var.get('a').put('runmsg', Js('')))
                PyJs_LONG_150_()
                var.put('b', var.get('angular').callprop('element', Js('#fileinput')))
                PyJsComma(PyJsComma(PyJsComma(var.get('b').callprop('wrap', Js('<form>')).callprop('closest', Js('form')).callprop('get', Js(0.0)).callprop('reset'),var.get('b').callprop('unwrap')),var.get('a').get('output').put('showresultstable', Js(1.0).neg())),var.get('a').put('data_toggle_label', (Js('Hide') if var.get('a').get('output').get('showresultstable') else Js('Show'))))
            PyJs_anonymous_149_._set_name('anonymous')
            @Js
            def PyJs_anonymous_151_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                PyJsComma(var.get('a').get('input').put('groupKeys', var.get('b').callprop('getGroupKeys')),var.get('a').get('input').put('group', var.get('a').get('input').get('groupKeys').get('0')))
            PyJs_anonymous_151_._set_name('anonymous')
            @Js
            def PyJs_anonymous_152_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('a').get('input').get('group')
                PyJsComma(PyJsComma(var.get('a').get('input').put('productKeys', var.get('b').callprop('getProductKeysForGroup', var.get('a').get('input').get('group'))),var.get('a').get('input').put('products', var.get('b').callprop('getProductsForGroup', var.get('a').get('input').get('group')))),var.get('a').get('input').put('product', var.get('a').get('input').get('products').get('0').get('id')))
                var.get('a').get('input').get('product')
                var.get('a').callprop('setCt')
            PyJs_anonymous_152_._set_name('anonymous')
            @Js
            def PyJs_anonymous_153_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['b', 'c'])
                var.put('b', var.get('a').get('input').get('group'))
                var.put('c', var.get('a').get('input').get('product'))
                def PyJs_LONG_155_(var=var):
                    def PyJs_LONG_154_(var=var):
                        return (var.get('a').get('input').put('ct', Js(500.0)) if (PyJsStrictEq(Js(0.0),var.get('c').callprop('indexOf', Js('phusion'))) or PyJsStrictEq(Js(0.0),var.get('c').callprop('indexOf', Js('q5')))) else (var.get('a').get('input').put('ct', Js(400.0)) if (PyJsStrictEq(Js(0.0),var.get('c').callprop('indexOf', Js('lataq'))) or PyJsStrictEq(Js(0.0),var.get('c').callprop('indexOf', Js('lahstaq')))) else var.get('a').get('input').put('ct', Js(200.0))))
                    return (var.get('a').get('input').put('ct', Js(500.0)) if (PyJsStrictEq(Js(0.0),var.get('b').callprop('indexOf', Js('Phusion'))) or PyJsStrictEq(Js(0.0),var.get('b').callprop('indexOf', Js('Q5')))) else (var.get('a').get('input').put('ct', Js(400.0)) if PyJsStrictEq(Js(0.0),var.get('b').callprop('indexOf', Js('LongAmp'))) else (PyJs_LONG_154_() if PyJsStrictEq(Js(0.0),var.get('b').callprop('indexOf', Js('Master'))) else var.get('a').get('input').put('ct', Js(200.0)))))
                PyJsComma(PyJs_LONG_155_(),var.get('a').callprop('runCalc3'))
            PyJs_anonymous_153_._set_name('anonymous')
            @Js
            def PyJs_anonymous_156_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['P', 'f', 'h', 'd', 'J', 'o', 'x', 'e', 'Q', 'N', 'w', 't', 'O', 'C', 'r', 'H', 'M', 'i', 'm', 's', 'y', 'K', 'g', 'A', 'n', 'G', 'l', 'k', 'z', 'F', 'j', 'D', 'v', 'q', 'E', 'B', 'L', 'I', 'u', 'p'])
                var.put('x', var.get('a').get('input').get('batch'))
                var.put('y', Js(''))
                var.put('z', Js(''))
                var.put('A', Js(''))
                var.put('B', Js(''))
                var.put('C', Js(''))
                var.put('D', (var.get('a').get('input').get('ct')/Js(1000.0)))
                var.put('E', var.get('a').get('input').get('product'))
                var.put('F', var.get('a').get('input').get('group'))
                var.put('G', Js([]))
                var.put('H', Js([]))
                var.put('I', Js(0.0))
                var.put('J', JsRegExp('/[\\t\\;]/'))
                var.put('K', Js(1.0).neg())
                var.put('L', Js(1.0))
                var.put('M', Js(0.0))
                var.put('N', var.get('x').callprop('split', JsRegExp('/\\n\\r?/')))
                PyJs_Object_157_ = Js({})
                PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').put('result', PyJs_Object_157_),var.get('a').put('output', Js([]))),var.get('a').put('ctstatus', Js(''))),var.get('a').put('runmsg', Js(''))),var.get('a').get('output').put('showresultstable', Js(1.0).neg())),var.get('a').put('data_toggle_label', (Js('Hide') if var.get('a').get('output').get('showresultstable') else Js('Show'))))
                #for JS loop
                var.put('O', Js(0.0))
                while (var.get('O')<var.get('N').get('length')):
                    try:
                        (var.get('N').get(var.get('O')).callprop('match', JsRegExp('/^\\s*$/')) and var.get('N').callprop('splice', var.get('O'), Js(1.0)))
                    finally:
                            var.put('O',Js(var.get('O').to_number())+Js(1))
                if PyJsComma((((var.get('N').get('length')>Js(1.0)) and (var.get('N').get('0').callprop('split', var.get('J')).get('length')<Js(4.0))) and PyJsComma(PyJsComma(var.put('K', Js(0.0).neg()),var.put('L', Js(2.0))),var.put('M', Js(1.0)))),((Js(0.0)>=var.get('D')) or var.get('isNaN')((var.get('D')/Js(1.0))))):
                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('i', Js(1.0).neg()),var.get('a').put('ctstatus', Js('invalidct'))),var.get('H').callprop('push', Js('Invalid primer concentration. '))),var.get('a').get('result').put('itemlist', var.get('G'))),var.get('a').get('result').put('critlist', var.get('H'))),PyJsComma(var.get('a').put('p1status', Js('')), Js(None)))
                while 1:
                    SWITCHED = False
                    CONDITION = (PyJsComma(PyJsComma(PyJsComma(var.put('f', var.get('b').callprop('getBufferIdForProduct', var.get('E'))),(PyJsStrictEq(Js('onetaq_gc'),var.get('f')) and var.put('I', Js(5.0)))),var.put('g', var.get('b').callprop('getBufferSaltForProduct', var.get('a').get('input').get('product')))),var.get('F')))
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('Phusion')):
                        SWITCHED = True
                        pass
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('Phusion Hot Start Flex')):
                        SWITCHED = True
                        var.put('h', Js(1.0))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('Master Mix')):
                        SWITCHED = True
                        var.put('h', (Js(1.0) if PyJsStrictEq(Js(0.0),var.get('E').callprop('indexOf', Js('phusion'))) else Js(4.0)))
                        break
                    if True:
                        SWITCHED = True
                        var.put('h', Js(4.0))
                    SWITCHED = True
                    break
                def PyJs_LONG_158_(var=var):
                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('r', var.get('b').callprop('validateBuffer', var.get('E'), var.get('F'), var.get('f'))),(var.get('r').get('hasCritWarnings') and var.get('Array').get('prototype').get('push').callprop('apply', var.get('H'), var.get('r').get('critwarnings')))),(var.get('r').get('hasWarnings') and var.get('Array').get('prototype').get('push').callprop('apply', var.get('G'), var.get('r').get('warnings')))),var.get('a').get('result').put('itemlist', var.get('G'))),var.get('a').get('result').put('critlist', var.get('H'))),var.get('c').callprop('setCt', var.get('D')).callprop('setSalt', var.get('g')).callprop('setMethod', var.get('h')).callprop('setDMSO', var.get('I'))),var.put('k', Js(0.0))),var.put('l', Js(0.0))),var.put('o', Js(0.0)))
                PyJs_LONG_158_()
                #for JS loop
                var.put('P', var.get('M'))
                while (var.get('P')<var.get('N').get('length')):
                    try:
                        if PyJsComma(PyJsComma(PyJsComma(var.put('C', Js('OK')),var.put('m', Js(1.0).neg())),var.put('n', Js(1.0).neg())),var.get('K')):
                            if PyJsComma(PyJsComma(var.put('d', var.get('N').get((var.get('P')-Js(1.0))).callprop('split', var.get('J'))),var.put('e', var.get('N').get(var.get('P')).callprop('split', var.get('J')))),((var.get('d').get('length')<Js(2.0)) or (var.get('e').get('length')<Js(2.0)))):
                                var.put('o',Js(var.get('o').to_number())+Js(1))
                                continue
                            PyJsComma(PyJsComma(PyJsComma(var.put('y', var.get('d').get('1')),var.put('A', var.get('d').get('0'))),var.put('z', var.get('e').get('1'))),var.put('B', var.get('e').get('0')))
                        else:
                            if PyJsComma(var.put('d', var.get('N').get(var.get('P')).callprop('split', var.get('J'))),(var.get('d').get('length')<Js(4.0))):
                                var.put('o',Js(var.get('o').to_number())+Js(1))
                                continue
                            PyJsComma(PyJsComma(PyJsComma(var.put('y', var.get('d').get('1')),var.put('z', var.get('d').get('3'))),var.put('A', var.get('d').get('0'))),var.put('B', var.get('d').get('2')))
                        def PyJs_LONG_162_(var=var):
                            def PyJs_LONG_159_(var=var):
                                return (PyJsComma(PyJsComma(var.put('v', var.get('c').callprop('Tm', var.get('y').callprop('replace', JsRegExp('/\\s/g'), Js(''))).get('tm')),var.put('v', var.get('Math').callprop('round', (var.get('Math').callprop('round', (Js(10.0)*var.get('v')))/Js(10.0))))),var.get('a').get('result').put('tm1', var.get('v'))) if PyJsStrictNeq(Js('invalidseq'),var.get('a').get('p1status')) else var.get('a').get('result').put('tm1', Js('---')))
                            def PyJs_LONG_160_(var=var):
                                return (PyJsComma(PyJsComma(var.put('w', var.get('c').callprop('Tm', var.get('z').callprop('replace', JsRegExp('/\\s/g'), Js(''))).get('tm')),var.put('w', var.get('Math').callprop('round', (var.get('Math').callprop('round', (Js(10.0)*var.get('w')))/Js(10.0))))),var.get('a').get('result').put('tm2', var.get('w'))) if PyJsStrictNeq(Js('invalidseq'),var.get('a').get('p2status')) else var.get('a').get('result').put('tm2', Js('---')))
                            def PyJs_LONG_161_(var=var):
                                return PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('u', var.get('b').callprop('getAnnealTemp', var.get('y'), var.get('v'), var.get('z'), var.get('w'), var.get('F'), var.get('E'))),var.get('a').get('result').put('ta', var.get('Math').callprop('round', var.get('u')))),var.put('q', var.get('b').callprop('validateTm', var.get('v'), var.get('w'), var.get('u'), var.get('E'), var.get('F'), var.get('f')))),(var.get('q').get('hasCritWarnings') and PyJsComma(var.put('n', Js(0.0).neg()),var.put('C', (Js('--')+var.get('q').get('critwarnings').callprop('join', Js('--'))), '+')))),(var.get('q').get('hasWarnings') and PyJsComma(var.put('n', Js(0.0).neg()),var.put('C', (Js('-- ')+var.get('q').get('warnings').callprop('join', Js('-- '))), '+'))))
                            return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').get('input').put('p1', var.get('y').callprop('toUpperCase')),var.get('a').get('input').put('p2', var.get('z').callprop('toUpperCase'))),var.get('a').get('input').put('id1', var.get('A'))),var.get('a').get('input').put('id2', var.get('B'))),var.put('p', var.get('b').callprop('validateInput', var.get('a').get('input').get('p1').callprop('replace', JsRegExp('/\\s/g'), Js('')), var.get('a').get('input').get('p2').callprop('replace', JsRegExp('/\\s/g'), Js('')), var.get('D'), var.get('E'), var.get('F')))),var.put('s', var.get('p').get('p1isValid'))),var.put('t', var.get('p').get('p2isValid'))),var.put('j', var.get('p').get('hasCritWarnings'))),var.get('a').put('p1status', var.get('p').get('p1status'))),var.get('a').put('p2status', var.get('p').get('p2status'))),(var.get('j') and PyJsComma(var.put('C', var.get('p').get('critwarnings').callprop('join', Js('-- '))),var.put('m', Js(0.0).neg())))),PyJs_LONG_159_()),PyJs_LONG_160_()),(PyJs_LONG_161_() if (PyJsStrictNeq(Js('invalidseq'),var.get('a').get('p1status')) and PyJsStrictNeq(Js('invalidseq'),var.get('a').get('p2status'))) else var.get('a').get('result').put('ta', Js('---')))),(var.get('m') and var.put('k', Js(1.0), '+'))),(var.get('n') and var.put('l', Js(1.0), '+'))),var.get('a').get('output').callprop('push', Js([var.get('a').get('input').get('id1'), var.get('a').get('input').get('p1'), var.get('a').get('result').get('tm1'), var.get('a').get('input').get('id2'), var.get('a').get('input').get('p2'), var.get('a').get('result').get('tm2'), var.get('a').get('result').get('ta'), var.get('C')]).callprop('join', Js('\t')))),var.get('a').put('p1status', Js('')))
                        PyJs_LONG_162_()
                    finally:
                            var.put('P', var.get('L'), '+')
                def PyJs_LONG_163_(var=var):
                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(((var.get('a').get('output').get('length')>Js(0.0)) and var.get('a').get('output').callprop('unshift', Js([Js('ID 1'), Js('Primer 1 sequence'), Js('Tm 1'), Js('ID 2'), Js('Primer 2 sequence'), Js('Tm 2'), Js('Anneal temp'), Js('Notes')]).callprop('join', Js('\t')))),(var.get('a').put('runmsg', (var.get('o')+Js(' Invalid line(s) '))) if (var.get('o')>Js(0.0)) else var.get('a').put('runmsg', Js('')))),var.get('a').put('runmsg', (((((var.get('a').get('output').get('length')-Js(1.0))+Js(' pair(s) processed. Errors: '))+var.get('k'))+Js(' Warnings: '))+var.get('l')), '+')),var.get('a').get('result').put('batch', var.get('a').get('output').callprop('join', Js('\n')))),var.get('a').get('result').put('batch2', Js([])))
                PyJs_LONG_163_()
                #for JS loop
                var.put('Q', Js(0.0))
                while (var.get('Q')<var.get('a').get('output').get('length')):
                    try:
                        var.get('a').get('result').get('batch2').callprop('push', var.get('a').get('output').get(var.get('Q')).callprop('split', Js('\t')))
                    finally:
                            var.put('Q',Js(var.get('Q').to_number())+Js(1))
                (var.get('a').put('novaliddatamsg', Js('Unable to detect format or no valid data entered -- check format of 1st line.')) if ((Js(0.0)==var.get('a').get('output').get('length')) and (var.get('N').get('length')>Js(0.0))) else var.get('a').put('novaliddatamsg', Js('')))
            PyJs_anonymous_156_._set_name('anonymous')
            @Js
            def PyJs_anonymous_164_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return var.get('a').get('result').get('batch')
            PyJs_anonymous_164_._set_name('anonymous')
            @Js
            def PyJs_anonymous_165_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers(['b', 'c', 'd'])
                var.put('b', var.get('a').callprop('getBatchResults'))
                var.put('c', Js('tmcalc_batch.txt'))
                PyJs_Object_166_ = Js({'type':Js('text/plain;charset=utf-8')})
                var.put('d', var.get('Blob').create(Js([var.get('b')]), PyJs_Object_166_))
                var.get('saveAs')(var.get('d'), var.get('c'))
            PyJs_anonymous_165_._set_name('anonymous')
            return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').put('prefill', PyJs_anonymous_147_),var.get('a').put('clearCalc', PyJs_anonymous_149_)),var.get('a').put('setGroups', PyJs_anonymous_151_)),var.get('a').put('setProducts', PyJs_anonymous_152_)),var.get('a').put('setCt', PyJs_anonymous_153_)),var.get('a').put('runCalc3', PyJs_anonymous_156_)),var.get('a').put('getBatchResults', PyJs_anonymous_164_)),var.get('a').put('downloadData', PyJs_anonymous_165_))
        PyJs_LONG_167_()
        @Js
        def PyJs_anonymous_168_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return Js('Product selections and sequence data will not be preserved if you leave this page.')
        PyJs_anonymous_168_._set_name('anonymous')
        var.put('i', PyJs_anonymous_168_)
        def PyJs_LONG_176_(var=var):
            @Js
            def PyJs_anonymous_169_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('i')()
            PyJs_anonymous_169_._set_name('anonymous')
            @Js
            def PyJs_anonymous_170_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('e').callprop('path', Js('#/about'))
            PyJs_anonymous_170_._set_name('anonymous')
            @Js
            def PyJs_anonymous_171_(a, this, arguments, var=var):
                var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
                var.registers(['b', 'a'])
                var.put('b', var.get(u"this").get('$root').get('$$phase'))
                (((var.get('a') and (Js('function')==var.get('a',throw=False).typeof())) and var.get('a')()) if ((Js('$apply')==var.get('b')) or (Js('$digest')==var.get('b'))) else var.get(u"this").callprop('$apply', var.get('a')))
            PyJs_anonymous_171_._set_name('anonymous')
            @Js
            def PyJs_anonymous_172_(b, this, arguments, var=var):
                var = Scope({'b':b, 'this':this, 'arguments':arguments}, var)
                var.registers(['b'])
                @Js
                def PyJs_anonymous_173_(this, arguments, var=var):
                    var = Scope({'this':this, 'arguments':arguments}, var)
                    var.registers([])
                    PyJsComma(PyJsComma(PyJsComma(var.get('a').get('input').put('batch', var.get('b')),var.get('a').get('output').put('showresultstable', Js(1.0).neg())),var.get('a').put('data_toggle_label', (Js('Hide') if var.get('a').get('output').get('showresultstable') else Js('Show')))),var.get('a').callprop('runCalc3'))
                PyJs_anonymous_173_._set_name('anonymous')
                var.get('a').callprop('safeApply', PyJs_anonymous_173_)
            PyJs_anonymous_172_._set_name('anonymous')
            @Js
            def PyJs_anonymous_174_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                var.get('e').callprop('path', Js('/'))
            PyJs_anonymous_174_._set_name('anonymous')
            @Js
            def PyJs_anonymous_175_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                PyJsComma(var.get('a').get('output').put('showresultstable', var.get('a').get('output').get('showresultstable').neg()),var.get('a').put('data_toggle_label', (Js('Hide') if var.get('a').get('output').get('showresultstable') else Js('Show'))))
            PyJs_anonymous_175_._set_name('anonymous')
            return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('a').callprop('$on', Js('$routeChangeStart'), PyJs_anonymous_169_),var.get('a').put('about', PyJs_anonymous_170_)),var.get('a').put('safeApply', PyJs_anonymous_171_)),var.get('a').put('processFileData', PyJs_anonymous_172_)),var.get('a').put('switch2single', PyJs_anonymous_174_)),var.get('a').put('toggle_data_display', PyJs_anonymous_175_)),var.get('a').get('output').put('showresultstable', Js(1.0).neg())),var.get('a').put('data_toggle_label', (Js('Hide') if var.get('a').get('output').get('showresultstable') else Js('Show')))),var.get('a').get('input').put('p1', var.get('g'))),var.get('a').get('input').put('p2', var.get('h'))),var.get('a').callprop('setGroups')),var.get('a').callprop('setProducts'))
        PyJs_LONG_176_()
    PyJs_anonymous_142_._set_name('anonymous')
    @Js
    def PyJs_anonymous_177_(a, this, arguments, var=var):
        var = Scope({'a':a, 'this':this, 'arguments':arguments}, var)
        var.registers(['a'])
        def PyJs_LONG_178_(var=var):
            return var.get('a').callprop('put', Js('views/about.204cf15b.html'), Js('<div id="one-true" class="row-fluid one-true"> <!-- <div id="sidebar-container" class="col-xs-1 one-true-col dnp">\r\n    </div> --> <div class="col-xs-8 col-xs-offset-1 one-true-col"> <a href="" ng-href="/#!/">Back to Home Page</a> <div class="filler"></div> <div id="aboutdescription" class="row-fluid aboutcontent"> <h4 class="orange">NEB Tm Calculator v{{appVersion}}</h4> <p>The NEB Tm calculator is intended for use in estimating the optimal annealing temperature for PCR with NEB polymerases. </p> <h4 class="orange">System Requirements</h4> <p>NEB Tm Calculator is best used on modern web browsers that are compliant with HTML5 and CSS3 standards. Javascript must be enabled for the tool to work. </p> <h4 class="orange">Privacy</h4> <p>NEB Tm Calculator does not store or transfer any user data to NEB servers. All calculations are handled within the user\'s browser. NEB Tm Calculator incorporates code from Google Analytics, which may transmit anonymous usage data (page access numbers and times, user IP, user browser version, etc.) to Google. </p> <h4 class="orange">Legal</h4> <p> <a href="https://www.neb.com/trademarks">Trademark information</a>. </p> <p> <a href="https://www.neb.com/patents">Patent information</a>. </p> <p> <a href="https://www.neb.com/about-neb/business-development-opportunities">Licensing information</a>. </p> </div> </div><!-- .content --> </div>'))
        def PyJs_LONG_179_(var=var):
            return var.get('a').callprop('put', Js('views/batch.03c23ef3.html'), Js('<div id="one-true" class="row one-true"> <div id="sidebar-container" class="col-sm-3 one-true-col dnp"> <div ng-include="\'views/batchsidebar.23048bea.html\'"></div> </div> <div class="col-sm-9 one-true-col"> <div class="row content"> <div id="input" class="col-sm-12"> <div class="row"> <!-- <div class="blue explain" ng-click="openmodal(\'tmchangenote\', \'md\')">Note: Recent changes to Tm calculations</div> --> <div class="col-sm-8"> <span class="fieldlabel">Product Group</span><br> <select ng-model="input.group" ng-options="gr for gr in input.groupKeys" ng-change="setProducts()"> <!-- <option ng-repeat="gr in input.groupKeys" value="{{gr}}">{{gr}}</option> --> </select><br> <span class="fieldlabel">Polymerase/Kit</span><br> <select ng-model="input.product" ng-options="pr.id as pr.name for pr in input.products" ng-change="setCt()"> <!-- <option ng-repeat="pr in input.productKeys" value="{{pr}}">{{pr}}</option> --> </select><br> </div> </div> <div class="row"> <div class="col-sm-8"> <div class="row"> <div class="col-sm-7"> <span class="fieldlabel">Primer Concentration (nM)</span><br> <input id="ct" ng-class="ctstatus" ng-model="input.ct" type="number" required ng-change="runCalc2()"> </div> <div class="col-sm-5"> <div class="dnp refresh-holder"> <span class="glyphicon glyphicon-refresh"></span> <a class="btn-link" ng-click="setCt()">Reset concentration </a> </div> </div> </div> </div> </div> <br> <div class="row"> <div class="col-sm-12"> <span class="fieldlabel">Primer Pairs</span><br> <textarea id="batchinput" ng-model="input.batch" ng-class="p1status" ng-change="runCalc3()" placeholder="ID#1 ; Primer1 ; ID#2 ; Primer2 -newline-">\r\n                        </textarea> <div id="fileinputcontainer"> <span>Load primer pairs from file: </span> <input type="file" fileinput processwith="processFileData(filedata)" ng-model="input.filename" id="fileinput"> </div> </div> </div> <div class="row"> <div class="col-sm-8"> <div class="row"> <div class="col-sm-7"> <a ng-click="switch2single()" class="btn-link dnp">Switch to single pair mode</a> </div> <div class="col-sm-5"> <a ng-click="clearCalc()" class="btn-link dnp">Clear</a> <br> <a ng-click="prefill()" class="btn-link dnp">Use example input</a> <br> </div> </div> </div> </div> <div class="row"> <div class="col-sm-12"> <div id="result" class="col-sm-12" ng-hide="output"> <span class="invalidseq">{{novaliddatamsg}}</span> </div> </div> </div> <div class="row"> <div class="col-sm-12"> <div id="result" ng-show="output.length"> <a ng-click="toggle_data_display()" class="btn-link dnp">{{data_toggle_label}} results</a> <a class="downloadfile" href="" ng-click="downloadData()"> <img ng-src="images/download3i.d680661d.png"> </a> <br> <div ng-hide="output.showresultstable"><h4>{{runmsg}}</h4></div> <table class="batchresultstable" ng-show="output.showresultstable"> <tr ng-repeat="row in result.batch2"> <td ng-repeat="idx in [0,1,2,3,4,5,6,7]" class="batchresultscell">{{row[idx]}}</td> </tr> </table> </div> </div> </div> </div> </div> <div class="row"> <div class="col-sm-11"> <hr> <div id="crit" class="notes"> <ul> <li ng-repeat="item in result.critlist">{{item}}</li> </ul> </div> <div id="warn" class="notes" ng-show="result.ta"> <ul> <li ng-repeat="item in result.itemlist">{{item}}</li> </ul> </div> </div> </div> </div> </div>'))
        def PyJs_LONG_180_(var=var):
            return var.get('a').callprop('put', Js('views/batchsidebar.23048bea.html'), Js('<div id="sidemenu" class="sidemenu"> <button id="toggle-sidebar" class="btn-link visible-phone" data-toggle="collapse" data-target="#sidebar-content"> <!-- <span class="icon-th-list"></span> --> <i class="icon-chevron-down"></i> </button> <div id="idebar-content" class="collapse in"> <p> Use the NEB Tm Calculator to estimate an appropriate annealing temperature when using NEB PCR products. </p><p> <strong>Instructions</strong> <ol> <li>Select the product group of the polymerase or kit you plan to use.</li> <li>Select the polymerase or kit from the list of products.</li> <li>If needed, modify the recommended primer concentration.</li> <li>Enter primer sequence pairs (ACGT only). Spaces allowed. Primer pairs (one pair per line) are expected to be in the format ID1 Primer1 ID2 Primer2, with values separated by semicolons. Data loaded from a plain text file or by copy/paste may also use tabs. </li> </ol> </p><p> Results can be downloaded in tab-delimited format as a plain text file in many modern browsers. In some browsers, file download will trigger display of the output in a new tab. <strong>Input lines that do not match the expected format are ignored.</strong> Please visit <a href="" ng-href="/#!/help">Help</a> for more information. </p> </div> </div>'))
        def PyJs_LONG_181_(var=var):
            return var.get('a').callprop('put', Js('views/help.ef501d45.html'), Js('<div id="one-true" class="row-fluid one-true"> <!-- <div id="sidebar-container" class="col-xs-1 one-true-col dnp">\r\n    </div> --> <div class="col-xs-8 col-xs-offset-1 one-true-col"> <a href="" ng-href="/#!/">Back to Home Page</a> <div class="filler"></div> <div id="helpdescription" class="row-fluid helpcontent"> <h4 class="orange">Help</h4> <p> The NEB Tm calculator is intended for use in estimating the optimal annealing temperature for PCR with NEB polymerases. Tm values are calculated using thermodynamic data from Santa Lucia [1] and the salt correction of Owczarzy [2]. For Phusion® DNA Polymerases, the thermodynamic data is from Breslauer et al. [3] and uses the salt correction of Schildkraut [2]. </p> <h4 class="orange">Batch Processing</h4> <p> In batch mode, the NEB Tm calculator will process multiple pairs of primer sequences and provide a tabular output. Primer pairs may be entered directly into the text box, copied and pasted into the text box, or loaded from a local file. In many modern browsers, a file can be dropped onto the file selection/browse button from the desktop. After processing, results may be downloaded in tab-delimited format as a plain text file. In some browsers (including Safari), file download will trigger display of the output in a new tab. The data may be copied from that tab or saved using the browser\'s <b>File Save As ...</b> menu function. Copy-to-clipboard functionality has been disabled as it relied on Flash plugins that are being blocked by many modern browsers. <strong>Note that input lines that do not match the expected format (see below) or have just a single sequence are skipped and not shown in the output.</strong> Errors and warnings are listed and attached to each line in the output. The output is best viewed by pasting it into a spreadsheet. </p> <p> Primer pairs (one pair per line) are expected to be in the following format: </p> <p> <em><strong>ID1</strong> [separator] <strong>Primer1 sequence</strong> [separator] <strong>ID2</strong> [separator] <strong>Primer2 sequence</strong></em> </p> <p> <tt> P1fwd AGCGGATAACAATTTCACACAGGA P1rev GTAAAACGACGGCCAGT <br> P1fwd; AGCGGATAACAATTTCACACAGGA; P1rev; GTAAAACGACGGCCAGT </tt> </p> <p> where the separators can be tabs or semicolons. Tab-separated (tsv) or semicolon-separated data exported from Microsoft Excel spreadsheets is acceptable. CSV (comma-separated files) will not work. The primer sequence must contain only A,C,G,T or spaces. <strong>Please note that tabs cannot be entered directly into the text area, so manual entry should use semicolons as separators. </strong> If the first input line contains only one primer, the data is assumed to be interleaved, with primer pairs split over subsequent lines. The entire input file must use the same format for input. </p> <h4 class="orange">How do I calculate just the Tm for a list of sequences (not pairs)?</h4> <p> The NEB Tm calculator is designed to recommend optimal annealing temperatures for primer pairs. To get Tm values for a list of single primers, enter them one per line (ID1; Sequence1) but append ;; (2 semicolons) after the primer sequence. The software will process the line as having an invalid second primer, but will calculate the Tm of the first primer. </p> <h4 class="orange">Why is the primer Tm (or annealing temperature) different from other Tm calculators?</h4> <p> The NEB Tm calculator is designed to take into account the buffer conditions of the amplification reaction based on the selected NEB polymerase. Many Tm calculators do not, relying instead on a default salt concentration. The annealing temperature for each polymerase is based on empirical observations of efficiency. The optimal annealing temperature for high fidelity hot start DNA polymerases like Q5 may differ significantly from that of Taq-based polymerases. </p> <h4 class="orange">Tm Calculation Method</h4> <p> The general format for `T_m` calculation is </p> <p style="text-align:center"> `T_m = (\\DeltaH^o)/(\\DeltaS^o + R * ln C_p) - 273.15` </p> <p> where `C_p` is the primer concentration, `DeltaH^o` is enthalpy (`cal*mol^-1`), `\\DeltaS^o` is entropy (`cal*K^-1*mol^-1`) and `R` is the universal gas constant (1.987`cal*K^-1*mol^-1`). `DeltaH^o` and `\\DeltaS^o` are computed from experimentally derived values for these parameters using the nearest-neighbor model, summing over all dinucleotides in the primer sequence. 273.15 is subtracted to convert from Kelvin to Celsius. </p> <p> In the NEB Tm Calculator, `T_m` is computed by the method of SantaLucia [1] as </p> <p style="text-align:center"> `T_m = ((\\DeltaH_i^o + \\DeltaH^o) * 1000)/(\\DeltaS_i^o + \\DeltaS^o + R * ln C_p) - 273.15` </p> <p> where the primer concentration `C_p` is assumed to be significantly greater (6x) than the target template concentration. `DeltaH^o` and `\\DeltaS^o` are computed using the nearest-neighbor model values outlined in [1]. `DeltaH_i^o` and `\\DeltaS_i^o` are adjustments for helix initiation [1]. The factor of 1000 is included to convert enthalpy values reported in `kcal*mol^-1` to `cal*mol^-1`. </p> <p> The `T_m`, as calculated above, assumes a 1 M monovalent cation concentration. This value is adjusted to reaction buffer conditions using the salt correction of Owczarzy as outlined in [2] </p> <p style="text-align:center"> `T_m` (corrected) `= 1 / (1 / T_m + [(4.29 * f_{gc} - 3.95) * ln(m) + 0.94 * (ln(m))^2] * 10^-5)` </p> <p> where `f_{gc}` is the fractional GC content, and `m` is the monovalent cation concentration. </p> <p> For Phusion® polymerases, `T_m` is computed by the method of Breslauer [3] as </p> <p style="text-align:center"> `T_m = ((\\DeltaH^o) * 1000)/(\\DeltaS_i^o + \\DeltaS^o + R * ln (C_p/4)) - 273.15` </p> <p> `DeltaH^o` and `\\DeltaS^o` are computed using the nearest-neighbor model values published in [3]. `\\DeltaS_i^o` is an adjustment for helix initiation [3]. The factor of 1000 is included to convert enthalpy values reported in `kcal*mol^-1` to `cal*mol^-1`. </p> <p> The `T_m` is adjusted to reaction buffer conditions using the salt correction of Schildkraut as outlined in [2] </p> <p style="text-align:center"> `T_m` (corrected) `= T_m + 16.6 * ln(m)` </p> <p> where `m` is the monovalent cation concentration. </p> <p> While the method and data of SantaLucia are preferred, it was necessary to use the Breslauer data and modified equations for annealing temperatures in reactions using Phusion® polymerases to allow compatibility with recommendations provided by Finnzymes Oy, now a part of Thermo Fisher Scientific. </p> <hr> <p> <small> <ol> <li>SantaLucia (1998) PNAS 95:1460-5</li> <li>Owczarzy et al (2004) Biochem 43:3537-54</li> <li>Breslauer et al (1986) Proc. Nat. Acad. Sci. 83:3746-50</li> </ol> </small> </p> </div> </div> </div> <script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=AM_HTMLorMML-full"></script>'))
        def PyJs_LONG_182_(var=var):
            return var.get('a').callprop('put', Js('views/main.9b69837c.html'), Js('<div id="one-true" class="row one-true"> <div id="sidebar-container" class="col-sm-3 one-true-col dnp"> <div ng-include="\'views/sidebar.7a38702b.html\'"></div> </div> <div class="col-sm-9 one-true-col"> <div class="row content"> <div id="input" class="col-sm-8"> <div class="row"> <!-- <span class="blue explain" ng-click="openmodal(\'tmchangenote\', \'md\')">Note: Recent changes to Tm calculations</span> --> <div class="col-sm-12"> <span class="fieldlabel">Product Group</span><br> <select ng-model="input.group" ng-options="gr for gr in input.groupKeys" ng-change="setProducts()"> <!-- <option ng-repeat="gr in input.groupKeys" value="{{gr}}">{{gr}}</option> --> </select><br> <span class="fieldlabel">Polymerase/Kit</span><br> <select ng-model="input.product" ng-options="pr.id as pr.name for pr in input.products" ng-change="setCt()"> <!-- <option ng-repeat="pr in input.productKeys" value="{{pr}}">{{pr}}</option> --> </select><br> </div> </div> <div class="row"> <div class="col-sm-7"> <span class="fieldlabel">Primer Concentration (nM)</span><br> <input id="ct" ng-class="ctstatus" ng-model="input.ct" type="number" required ng-change="runCalc2()"> </div> <div class="col-sm-5"> <div class="dnp refresh-holder"> <span class="glyphicon glyphicon-refresh"></span> <a class="btn-link" ng-click="setCt()">Reset concentration </a> </div> </div> </div> <div class="row"> <div class="col-sm-12"> <span class="fieldlabel">Primer 1</span><br> <input id="p1" ng-model="input.p1" type="text" ng-class="p1status" ng-change="runCalc2()" placeholder="Primer 1 Sequence"> <span class="fieldlabel">Primer 2</span><br> <input id="p2" ng-model="input.p2" type="text" ng-class="p2status" ng-change="runCalc2()" placeholder="Primer 2 Sequence"> </div> </div> <br> <div class="row"> <div class="col-sm-7"> <a ng-click="switch2batch()" class="btn-link dnp">Switch to batch mode</a> </div> <div class="col-sm-5"> <a ng-click="clearCalc()" class="btn-link dnp">Clear</a> <br> <a ng-click="prefill()" class="btn-link dnp">Use example input</a> <br> </div> </div> </div> <div id="result" class="col-sm-4"> <div id="ta" class="answer" ng-show="result.ta"> <strong>Anneal at</strong><br> <h2>{{result.ta}} &deg;C</h2> </div> <div id="tm1" class="answer"> <div class="tiny-label">Primer 1</div> <div ng-show="result.tm1"> <strong>{{result.len1}} nt</strong><br> <strong>{{result.gc1}}% GC</strong><br> <strong>Tm: {{result.tm1}} &deg;C</strong> </div> </div> <div id="tm2" class="answer"> <div class="tiny-label">Primer 2</div> <div ng-show="result.tm2"> <strong>{{result.len2}} nt</strong><br> <strong>{{result.gc2}}% GC</strong><br> <strong>Tm: {{result.tm2}} &deg;C</strong> </div> </div> </div> </div> <!-- <div class="container-fluid"> --> <div class="row"> <div class="col-sm-8"> <hr> <div id="crit" class="notes"> <ul> <li ng-repeat="item in result.critlist">{{item}}</li> </ul> </div> <div id="warn" class="notes" ng-show="result.ta"> <ul> <li ng-repeat="item in result.itemlist">{{item}}</li> </ul> </div> </div> </div> <!-- </div> --> </div> </div> '))
        def PyJs_LONG_183_(var=var):
            return var.get('a').callprop('put', Js('views/modals/tmchangenote.html'), Js('<div class="modal-header"> <h4 class="modal-title">Recent changes to Tm calculations</h4> </div> <div class="modal-body"> <p> The calculations in the NEB Tm calculator were recently modified to correct an error that was decreasing the effective primer concentration to one quarter of it\'s input value. The correction raises Tm values by roughly 2&deg;C for all polymerase reaction buffers except Phusion, which uses a different algorithm. The recommended annealing temperature for reactions using Q5 polymerases has been adjusted, and reported values will be nearly the same as before the correction. The values for Taq-related polymerases were not adjusted, as the broad activity profile for these enzymes accommodates the changes without detrimental effects to yield. Please contact NEB technical support if you need additional guidance. </p> </div> <div class="modal-footer"> <button class="btn orange-btn" ng-click="modalOptions.ok()">OK</button> </div>'))
        def PyJs_LONG_184_(var=var):
            return var.get('a').callprop('put', Js('views/sidebar.7a38702b.html'), Js('<div id="sidemenu" class="sidemenu"> <button id="toggle-sidebar" class="btn-link visible-phone" data-toggle="collapse" data-target="#sidebar-content"> <!-- <span class="icon-th-list"></span> --> <i class="icon-chevron-down"></i> </button> <div id="sidebar-content" class="collapse in"> <p> Use the NEB Tm Calculator to estimate an appropriate annealing temperature when using NEB PCR products. </p><p> <strong>Instructions</strong> <ol> <li>Select the product group of the polymerase or kit you plan to use.</li> <li>Select the polymerase or kit from the list of products.</li> <li>If needed, modify the recommended primer concentration.</li> <li>Enter primer sequences (ACGT only) that anneal to the template. Spaces allowed. </li> </ol> </p><p> Note that an anealing temperature will only be displayed if both primer sequences are entered. </p> </div> </div>'))
        PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJs_LONG_178_(),PyJs_LONG_179_()),PyJs_LONG_180_()),PyJs_LONG_181_()),PyJs_LONG_182_()),PyJs_LONG_183_()),PyJs_LONG_184_())
    PyJs_anonymous_177_._set_name('anonymous')
    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('NEB').put('createTmCalc', PyJs_anonymous_61_),var.get('angular').callprop('module', Js('tmcApp')).callprop('factory', Js('tmcalc'), PyJs_anonymous_81_)),var.get('angular').callprop('module', Js('tmcApp')).callprop('factory', Js('tmcalculatorData'), Js([Js('$http'), PyJs_anonymous_83_]))),var.get('angular').callprop('module', Js('tmcApp')).callprop('controller', Js('MainCtrl'), Js([Js('$scope'), Js('tmcalculatorData'), Js('tmcalc'), Js('$routeParams'), Js('$location'), Js('$window'), PyJs_anonymous_115_]))),var.get('angular').callprop('module', Js('tmcApp')).callprop('controller', Js('AboutCtrl'), Js([Js('$scope'), PyJs_anonymous_141_]))),var.get('angular').callprop('module', Js('tmcApp')).callprop('controller', Js('BatchCtrl'), Js([Js('$scope'), Js('tmcalculatorData'), Js('tmcalc'), Js('$routeParams'), Js('$location'), Js('$window'), PyJs_anonymous_142_]))),var.get('angular').callprop('module', Js('tmcApp')).callprop('run', Js([Js('$templateCache'), PyJs_anonymous_177_])))
PyJs_LONG_185_()
pass


# Add lib to the module scope
neb_calc_tm = var.to_python()