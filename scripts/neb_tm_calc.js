"use strict";
angular.module("tmcApp", ["ngAnimate", "ngCookies", "ngResource", "ngRoute", "ngSanitize", "ngTouch", "ui.bootstrap"]).run(["$rootScope", "$modal", "modalService", function(a, b, c) {
    jQuery.event.props.push("dataTransfer"), a.appVersion = "1.9.5", a.openmodal = function(a, b) {
        var d = {
            templateUrl: "views/modals/" + a + ".html",
            size: b
        };
        c.showModal(d, {})
    }
}]).directive("fileinput", function() {
    return {
        restrict: "A",
        replace: !0,
        scope: {
            processwith: "&"
        },
        template: '<div><div></div><input type="file" /></div>',
        link: function(a, b) {
            var c = angular.element(b.children().eq(1)),
                d = function(a) {
                    a.stopPropagation(), a.preventDefault(), a.dataTransfer.dropEffect = "copy"
                },
                e = function(b) {
                    var c = new FileReader;
                    c.onload = function(b) {
                        console.log("about to call processwith"), console.log(b.target.result), console.log(a.processwith), a.processwith({
                            filedata: b.target.result
                        }), console.log("after call to processwith")
                    }, c.readAsText((b.srcElement || b.target).files[0])
                };
            c.on("dragover", d), c.on("drop", e), c.on("change", e)
        }
    }
}).directive("onReadFile", ["$parse", function(a) {
    return {
        restrict: "A",
        scope: !1,
        link: function(b, c, d) {
            var e = a(d.onReadFile);
            c.on("change", function(a) {
                var c = new FileReader;
                c.onload = function(a) {
                    b.$apply(function() {
                        e(b, {
                            filedata: a.target.result
                        })
                    })
                }, c.readAsText((a.srcElement || a.target).files[0])
            })
        }
    }
}]).config(["$locationProvider", function(a) {
    a.html5Mode(!1), a.hashPrefix("!")
}]).config(["$routeProvider", "$locationProvider", function(a, b) {
    b.html5Mode(!1), a.when("/", {
        templateUrl: "views/main.9b69837c.html",
        controller: "MainCtrl",
        resolve: {
            dataloaded: ["tmcalculatorData", function(a) {
                return a.promise
            }]
        }
    }).when("/testbs", {
        templateUrl: "views/testbs.html",
        controller: "TestbsCtrl"
    }).when("/about", {
        templateUrl: "views/about.204cf15b.html",
        controller: "AboutCtrl"
    }).when("/help", {
        templateUrl: "views/help.ef501d45.html",
        controller: "AboutCtrl"
    }).when("/batch", {
        templateUrl: "views/batch.03c23ef3.html",
        controller: "BatchCtrl",
        resolve: {
            dataloaded: ["tmcalculatorData", function(a) {
                return a.promise
            }]
        }
    }).when("/:p1seq/:p2seq", {
        templateUrl: "views/main.9b69837c.html",
        controller: "MainCtrl",
        resolve: {
            dataloaded: ["tmcalculatorData", function(a) {
                return a.promise
            }]
        }
    }).when("/:p1seq", {
        templateUrl: "views/main.9b69837c.html",
        controller: "MainCtrl",
        resolve: {
            dataloaded: ["tmcalculatorData", function(a) {
                return a.promise
            }]
        }
    }).when("/about", {
        templateUrl: "views/about.204cf15b.html",
        controller: "AboutCtrl",
        controllerAs: "about"
    }).when("/about", {
        templateUrl: "views/about.204cf15b.html",
        controller: "AboutCtrl",
        controllerAs: "about"
    }).otherwise({
        redirectTo: "/"
    })
}]), angular.module("tmcApp").factory("modalService", ["$http", "$modal", function(a, b) {
    var c = {
            backdrop: !0,
            keyboard: !0,
            modalFade: !0
        },
        d = {},
        e = {};
    return e.showModal = function(a, b) {
        return a || (a = {}), a.backdrop = !0, this.show(a, b)
    }, e.show = function(a, e) {
        var f = {},
            g = {};
        return angular.extend(f, c, a), angular.extend(g, d, e), f.controller || (f.controller = ["$scope", "$modalInstance", function(a, b) {
            a.modalOptions = g, a.modalOptions.close = function() {
                b.close("done")
            }, a.modalOptions.ok = function() {
                b.close("done")
            }
        }]), b.open(f).result
    }, e
}]);
var NEB = NEB || {};
NEB.trim = function(a) {
    a = a.replace(/^\s+/, "");
    for (var b = a.length - 1; b >= 0; b--)
        if (/\S/.test(a.charAt(b))) {
            a = a.substring(0, b + 1);
            break
        }
    return a
}, NEB.revcomp = function(a) {
    var b, c, d = "ACGTUKMSWRYBDHVNacgtukmswrybdhvn",
        e = "TGCAAMKWSYRVHDBNtgcaamkwsyrvhdbn",
        f = a.split("").reverse();
    for (b = 0; b < f.length; ++b) {
        if (c = d.indexOf(f[b]), -1 === c) throw {
            name: "InvalidCharacter",
            message: "A non IUPAC base was encountered"
        };
        f[b] = e.charAt(c)
    }
    return f.join("")
}, NEB.isValidSeq = function(a, b) {
    var c = " acgt";
    c += c.toUpperCase();
    var d = " acgtwsrymkbdhvn";
    d += d.toUpperCase();
    var e, f;
    for (e = b === !1 ? c : d, f = 0; f < a.length; ++f)
        if (-1 === e.indexOf(a.charAt(f))) return !1;
    return !0
}, NEB.isNumeric = function(a) {
    var b;
    return b = a / 1, !isNaN(b)
}, NEB.dmsg = function(a) {
    "undefined" != typeof console && "function" == typeof console.log && console.log(a)
};
var NEB = NEB || {};
NEB.createTmCalc = function(a) {
    var b = null,
        c = a.ct || .25,
        d = a.salt || 50,
        e = a.dmso || 0,
        f = a.methodid || 4,
        g = .001 * d,
        h = 1.987,
        i = {
            aa: -24,
            tt: -24,
            at: -23.9,
            ta: -16.9,
            ca: -12.9,
            tg: -12.9,
            gt: -17.3,
            ac: -17.3,
            ct: -20.8,
            ag: -20.8,
            ga: -13.5,
            tc: -13.5,
            cg: -27.8,
            gc: -26.7,
            gg: -26.6,
            cc: -26.6
        },
        j = {
            aa: -22.2,
            tt: -22.2,
            at: -20.4,
            ta: -21.3,
            ca: -22.7,
            tg: -22.7,
            gt: -22.4,
            ac: -22.4,
            ct: -21,
            ag: -21,
            ga: -22.2,
            tc: -22.2,
            cg: -27.2,
            gc: -24.4,
            gg: -19.9,
            cc: -19.9
        },
        k = {
            aa: -9.1,
            tt: -9.1,
            at: -8.6,
            ta: -6,
            ca: -5.8,
            tg: -5.8,
            gt: -6.5,
            ac: -6.5,
            ct: -7.8,
            ag: -7.8,
            ga: -5.6,
            tc: -5.6,
            cg: -11.9,
            gc: -11.1,
            gg: -11,
            cc: -11
        },
        l = {
            aa: -7.9,
            tt: -7.9,
            at: -7.2,
            ta: -7.2,
            ca: -8.5,
            tg: -8.5,
            gt: -8.4,
            ac: -8.4,
            ct: -7.8,
            ag: -7.8,
            ga: -8.2,
            tc: -8.2,
            cg: -10.6,
            gc: -9.8,
            gg: -8,
            cc: -8
        },
        m = !0,
        n = 0,
        o = null,
        p = null,
        q = 0,
        r = 0,
        s = 0,
        t = 0,
        u = 0,
        v = function() {
            this.sc_sch = 16.6 * Math.log(this.saltc) / Math.LN10, this.sc_sl = .368 * this.wseq.length * Math.log(this.saltc), this.sc_ow = 1e-5 * (4.29 * this.fgc - 3.95) * Math.log(this.saltc) + 94e-7 * Math.log(this.saltc) * Math.log(this.saltc)
        },
        w = function(a) {
            return this.method = a, this
        },
        x = function(a) {
            var b;
            if (!a) throw {
                name: "Missing seq",
                message: "setSeq: no sequence provided"
            };
            for (this.seq = a, this.wseq = NEB.trim(this.seq.toLowerCase().replace(" ", "")), this.cseq = NEB.revcomp(this.wseq), this.sym = this.wseq === this.cseq ? !0 : !1, this.primerc = 1e-6 * this.ct, this.gc_cnt = 0, b = 0; b < this.wseq.length; ++b)("g" === this.wseq.charAt(b) || "c" === this.wseq.charAt(b)) && (this.gc_cnt += 1);
            return this.fgc = this.gc_cnt / this.wseq.length, this.saltCorrect(), this
        },
        y = function(a) {
            return this.ct = a, this.primerc = 1e-6 * this.ct, this
        },
        z = function(a) {
            return this.salt = a, this.saltc = .001 * this.salt, this
        },
        A = function(a) {
            return this.dmso = a, this
        },
        B = function(a) {
            if (!a || "" === a) throw {
                name: "Missing seq",
                message: "calcTm: A sequence must be present to calculate Tm"
            };
            this.setSeq(a), this.saltCorrect();
            var b, c, d = 0,
                e = 0,
                f = 0,
                g = 0,
                h = 0,
                i = 0,
                j = this.primerc;
            switch (this.method) {
                case 1:
                    for (g += this.sym ? -12.4 : -10.8, b = 0; b < this.wseq.length - 1; ++b) c = this.wseq.slice(b, b + 2), e += this.dSBr[c], f += this.dHBr[c];
                    f *= 1e3, j /= 4, d = f / (g + e + this.R * Math.log(j)) - 273.15 + this.sc_sch;
                    break;
                case 3:
                case 4:
                    for (i = this.sym ? -1.4 : 0, ("a" === this.wseq.charAt(0) || "t" === this.wseq.charAt(0)) && (g += 4.1, h += 2300), ("a" === this.wseq.charAt(this.wseq.length - 1) || "t" === this.wseq.charAt(this.wseq.length - 1)) && (g += 4.1, h += 2300), ("g" === this.wseq.charAt(0) || "c" === this.wseq.charAt(0)) && (g += -2.8, h += 100), ("g" === this.wseq.charAt(this.wseq.length - 1) || "c" === this.wseq.charAt(this.wseq.length - 1)) && (g += -2.8, h += 100), b = 0; b < this.wseq.length - 1; b++) c = this.wseq.slice(b, b + 2), e += this.dSSa[c], f += this.dHSa[c];
                    f *= 1e3, d = (f + h) / (g + i + e + this.R * Math.log(j)), 3 === this.method ? d = 1 / (1 / d + this.sc_sl / (f + h)) : 4 === this.method && (d = 1 / (1 / d + this.sc_ow)), d -= 273.15;
                    break;
                case 7:
                    d = 81.5 + 16.6 * Math.log(this.saltc) / Math.LN10 + .41 * this.fgc - 675 / this.wseq.length
            }
            return d -= .6 * this.dmso, {
                method: this.method,
                wseq: this.wseq,
                tm: d,
                dh: f,
                ds: e,
                salt: this.saltc,
                ct: this.primerc,
                dmso: this.dmso,
                fgc: this.fgc,
                len: this.wseq.length
            }
        };
    return {
        setSeq: x,
        setSalt: z,
        setCt: y,
        setDMSO: A,
        setMethod: w,
        saltCorrect: v,
        Tm: B,
        gc_cnt: q,
        fgc: r,
        sc_sch: s,
        sc_sl: t,
        sc_ow: u,
        seq: b,
        ct: c,
        salt: d,
        dmso: e,
        method: f,
        wseq: o,
        cseq: p,
        sym: m,
        primerc: n,
        saltc: g,
        R: h,
        dSSa: j,
        dHSa: l,
        dSBr: i,
        dHBr: k
    }
}, angular.module("tmcApp").factory("tmcalc", function() {
    var a = NEB.createTmCalc({});
    return a
}), angular.module("tmcApp").factory("tmcalculatorData", ["$http", function(a) {
    var b = null,
        c = "tmcdata/tmcalculatordata.json",
        d = a.get(c).then(function(a) {
            b = a.data
        }),
        e = {
            saveddata: {},
            promise: d,
            tmcdata: b,
            getData: function() {
                return b
            },
            getGroups: function() {
                return b.groups
            },
            getGroupKeys: function() {
                var a, c = [];
                for (a in b.groups) b.groups.hasOwnProperty(a) && c.push(a);
                return c
            },
            getProducts: function() {
                return b.prods
            },
            getBuffers: function() {
                return b.buffs
            },
            getBufferSaltForProduct: function(a) {
                return b.buffs[b.prods[a].buffer]
            },
            getBufferIdForProduct: function(a) {
                return b.prods[a].buffer
            },
            getProductsForGroup: function(a) {
                for (var c, d = b.groups[a], e = [], f = 0; f < d.length; ++f) c = b.prods[d[f]], c.id = d[f], e.push(c);
                return e
            },
            getProductKeysForGroup: function(a) {
                var c, d = [],
                    e = b.groups[a];
                for (c in e) d.push(b.prods[e[c]].name);
                return d
            },
            getPropsForProduct: function(a) {
                return b.prods[a]
            },
            saveUserPrefs: function(a) {
                this.saveddata = a
            },
            restoreUserPrefs: function() {
                return this.savedata
            },
            validateInput: function(a, b, c, d, e) {
                var f = [],
                    g = !1,
                    h = [],
                    i = !1,
                    j = a.length,
                    k = b.length,
                    l = !0,
                    m = !0,
                    n = !0,
                    o = "",
                    p = "";
                return (0 >= c || isNaN(c / 1)) && (l = !1, g = !0, f.push("Invalid primer concentration. ")), .5 > c && -1 !== e.indexOf("Phusion") ? h.push("The recommended primer concentration for Phusion reactions is 500 nM.") : .4 > c && -1 !== e.indexOf("LongAmp") ? h.push("The recommended primer concentration for LongAmp reactions is 400 nM.") : .2 > c && h.push("The recommended primer concentration is 200 nM."), m = NEB.isValidSeq(a, !1), n = NEB.isValidSeq(b, !1), m || n ? (m || (f.push("Primer 1 has invalid bases. "), g = !0, o = "invalidseq"), n || (f.push("Primer 2 has invalid bases. "), g = !0, p = "invalidseq")) : (f.push("Both primers have invalid bases. "), g = !0, o = "invalidseq", p = "invalidseq"), 0 === j && (f.push("Primer 1 missing. "), g = !0, o = "invalidseq"), 0 === k && (f.push("Primer 2 missing. "), g = !0, p = "invalidseq"), (8 > j || 8 > k) && ((j > 0 || k > 0) && (f.push("Both primers need to be longer than 7 nt"), g = !0), 8 > j && (o = "invalidseq"), 8 > k && (p = "invalidseq")), {
                    hasWarnings: i,
                    warnings: h,
                    hasCritWarnings: g,
                    critwarnings: f,
                    ctisValid: l,
                    p1isValid: m,
                    p2isValid: n,
                    p1status: o,
                    p2status: p
                }
            },
            validateTm: function(a, b, c, d, e) {
                var f = [],
                    g = [];
                return (a - b) * (a - b) > 25 && g.push("Tm difference is greater than the recommended limit of 5 °C. "), "" !== c && 50 > c && -1 !== e.indexOf("Q5") ? g.push(" Annealing temperature is lower than the recommended minimum of 50 °C.") : "" !== c && 45 > c && g.push(" Annealing temperature is lower than the recommended minimum of 45 °C."), "" !== c && c >= 65 && (a > c || b > c) && ("Phusion" === e || "Vent" === e || "Deep Vent" === e || "Phusion Flex" === e || -1 !== e.indexOf("Q5") ? c >= 72 && f.push("Annealing temperature for experiments with this enzyme should typically not exceed 72°C.") : "LongAmp Taq" === e || "LongAmp Hot Start Taq" === e ? c >= 65 && f.push("Annealing temperature for experiments with this enzyme should typically not exceed 65°C.") : c >= 68 && f.push("Annealing temperature for experiments with this enzyme should typically not exceed 68°C.")), {
                    hasWarnings: f.length > 0,
                    warnings: f,
                    hasCritWarnings: g.length > 0,
                    critwarnings: g
                }
            },
            validateBuffer: function(a, b, c) {
                var d = [],
                    e = [];
                return "phusion_gc" === c || "onetaq_gc" === c || "phusionflex_gc" === c ? d.push("DMSO can improve PCR amplification from GC-rich templates,  but it is also known to reduce the annealing temperature of primers in a PCR reaction. Therefore,  it is recommended that for every 1% of additional DMSO added, the calculated annealing temperature should be reduced by 0.6°C [Chester and Marshak,  1993. Analytical Biochemistry 209,  284-290].") : "q5" === c && d.push("Use of the Q5 High GC Enhancer often lowers the range of temperatures at which specific amplification can be observed, however the rule used to determine Q5 annealing temperatures (Ta = Tm_lower+1°C) typically yields values that will support specific amplification with or without the enhancer."), {
                    hasWarnings: d.length > 0,
                    warnings: d,
                    hasCritWarnings: e.length > 0,
                    critwarnings: e
                }
            },
            getAnnealTemp: function(a, b, c, d, e, f) {
                var g, h, i, j = a.replace(/\s/g, "").length,
                    k = c.replace(/\s/g, "").length;
                switch (h = d > b ? b : d, i = k > j ? j : k, g = h, e) {
                    case "Taq DNA Polymerase":
                    case "Hemo KlenTaq":
                    case "OneTaq":
                    case "OneTaq Hot Start":
                    case "EpiMark Hot Start":
                    case "Hot Start Taq":
                        i > 7 && (g = h - 5), g > 68 && (g = 68);
                        break;
                    case "LongAmp Taq":
                    case "LongAmp Hot Start Taq":
                        i > 7 && (g = h - 5), g > 65 && (g = 65);
                        break;
                    case "Vent":
                    case "Deep Vent":
                        i > 20 && (g = h - 2), g > 72 && (g = 72);
                        break;
                    case "Phusion":
                    case "Phusion Hot Start Flex":
                        i > 20 && (g = h + 3), g > 72 && (g = 72);
                        break;
                    case "Q5":
                    case "Q5 Hot Start":
                        i > 7 && (g = h + 1), g > 72 && (g = 72);
                        break;
                    case "Master Mix":
                        0 === f.indexOf("q5") ? (i > 7 && (g = h + 1), g > 72 && (g = 72)) : 0 === f.indexOf("phusion") ? (i > 20 && (g = h + 3), g > 72 && (g = 72)) : 0 === f.indexOf("vent") || 0 === f.indexOf("deepvent") ? (i > 20 && (g = h - 2), g > 72 && (g = 72)) : (i > 7 && (g = h - 5), g > 68 && (g = 68));
                        break;
                    default:
                        g = h
                }
                return Math.round(10 * g) / 10
            }
        };
    return e
}]), angular.module("tmcApp").controller("MainCtrl", ["$scope", "tmcalculatorData", "tmcalc", "$routeParams", "$location", "$window", function(a, b, c, d, e) {
    a.input = {}, a.result = {}, a.input.p1 = "", a.input.p2 = "", a.input.ct = .25, a.result.tm1 = null, a.result.tm2 = null, a.result.len1 = "---", a.result.len2 = "---", a.result.gc1 = "---", a.result.gc2 = "---", a.result.ta = "---", a.result.itemlist = [], a.result.critlist = [], a.input.groupKeys = [], a.input.products = {}, a.input.prodKeys = [], a.input.group = "", a.input.product = "", a.p1status = "", a.p2status = "", b.restoreUserPrefs() ? (a.lastp1 = b.restoreUserPrefs().p1, a.lastp2 = b.restoreUserPrefs().p2) : (a.lastp1 = "", a.lastp2 = "");
    var f = d.p1seq || a.lastp1 || "",
        g = d.p2seq || a.lastp2 || "";
    a.prefill = function() {
        a.input.p1 = "AGCGGATAACAATTTCACACAGGA", a.input.p2 = "GTA AAA CGA CGG CCA GT", a.runCalc2()
    }, a.clearCalc = function() {
        a.input.p1 = "", a.input.p2 = "", a.result.tm1 = null, a.result.tm2 = null, a.result.len1 = "---", a.result.len2 = "---", a.result.gc1 = "---", a.result.gc2 = "---", a.result.ta = "---", a.result.itemlist = [], a.result.critlist = [], a.p1status = "", a.p2status = ""
    }, a.setGroups = function() {
        a.input.groupKeys = b.getGroupKeys(), a.input.group = a.input.groupKeys[0]
    }, a.setProducts = function() {
        var c, d;
        c = a.input.group, a.input.productKeys = b.getProductKeysForGroup(c), a.input.products = b.getProductsForGroup(c), a.input.product = a.input.products[0].id, d = a.input.product, a.setCt()
    }, a.setCt = function() {
        var b = a.input.group,
            c = a.input.product;
        0 === b.indexOf("Phusion") || 0 === b.indexOf("Q5") ? a.input.ct = 500 : 0 === b.indexOf("LongAmp") ? a.input.ct = 400 : 0 === b.indexOf("Master") ? 0 === c.indexOf("phusion") || 0 === c.indexOf("q5") ? a.input.ct = 500 : 0 === c.indexOf("lataq") || 0 === c.indexOf("lahstaq") ? a.input.ct = 400 : a.input.ct = 200 : a.input.ct = 200, a.runCalc2()
    }, a.runCalc2 = function() {
        var d, e, f, g, h, i, j, k, l, m, n = a.input.p1,
            o = a.input.p2,
            p = a.input.ct / 1e3,
            q = a.input.product,
            r = a.input.group,
            s = NEB.isNumeric(p),
            t = [],
            u = [],
            v = 0,
            w = NEB.isValidSeq(n, !1),
            x = NEB.isValidSeq(o, !1),
            y = b.validateInput(n.replace(/\s/g, ""), o.replace(/\s/g, ""), p, q, r);
        if (s = y.ctisValid, w = y.p1isValid, x = y.p2isValid, h = y.hasCritWarnings, g = y.hasWarnings, u = y.critwarnings, t = y.warnings, a.p1status = y.p1status, a.p2status = y.p2status, a.result.itemlist = t, a.result.critlist = u, a.ctstatus = "", !s) return a.result.ta = "---", a.result.tm1 = null, a.result.tm2 = null, a.ctstatus = "invalidct", w && (a.p1status = ""), void(x && (a.p2status = ""));
        if ("invalidseq" === a.p1status && "invalidseq" === a.p2status) return a.result.tm1 = null, a.result.tm2 = null, a.result.len1 = "---", a.result.len2 = "---", a.result.gc1 = "---", a.result.gc2 = "---", a.result.ta = "---", w && (a.p1status = ""), void(x && (a.p2status = ""));
        switch ("invalidseq" === a.p1status && (a.result.tm1 = null, a.result.len1 = "---", a.result.gc1 = "---", a.result.ta = "---"), "invalidseq" === a.p2status && (a.result.tm2 = null, a.result.len2 = "---", a.result.gc2 = "---", a.result.ta = "---"), d = b.getBufferIdForProduct(q), "onetaq_gc" === d && (v = 5), e = b.getBufferSaltForProduct(a.input.product), r) {
            case "Phusion":
            case "Phusion Hot Start Flex":
                f = 1;
                break;
            case "Master Mix":
                f = 0 === q.indexOf("phusion") ? 1 : 4;
                break;
            default:
                f = 4
        }
        if ("invalidseq" !== a.p1status && (l = c.setCt(p).setSalt(e).setMethod(f).setDMSO(v).Tm(n.replace(/\s/g, "")), j = l.tm, j = Math.round(Math.round(10 * j) / 10), a.result.tm1 = j, a.result.len1 = l.len, a.result.gc1 = 100 * l.fgc, a.result.gc1 = Math.round(10 * a.result.gc1 / 10)), "invalidseq" !== a.p2status && (m = c.setCt(p).setSalt(e).setMethod(f).setDMSO(v).Tm(o.replace(/\s/g, "")), k = m.tm, k = Math.round(Math.round(10 * k) / 10), a.result.tm2 = k, a.result.len2 = m.len, a.result.gc2 = 100 * m.fgc, a.result.gc2 = Math.round(10 * a.result.gc2 / 10)), "invalidseq" === a.p1status || "invalidseq" === a.p2status) return void(a.result.ta = "---");
        i = b.getAnnealTemp(n, j, o, k, r, q), a.result.ta = Math.round(i);
        var z = b.validateTm(j, k, i, q, r, d),
            A = b.validateBuffer(q, r, d);
        u = [], t = [], z.hasCritWarnings && (u = z.critwarnings), z.hasWarnings && (t = z.warnings), A.hasCritWarnings && Array.prototype.push.apply(u, A.critwarnings), A.hasWarnings && Array.prototype.push.apply(t, A.warnings), a.result.itemlist = t, a.result.critlist = u
    };
    var h = function() {
        return "Product selections and sequence data will not be preserved if you leave this page."
    };
    a.$on("$routeChangeStart", function() {
        h()
    }), a.about = function() {
        e.path("#/about")
    }, a.switch2batch = function() {
        e.path("/batch")
    }, a.input.p1 = f, a.input.p2 = g, a.setGroups(), a.setProducts(), a.clearCalc()
}]), angular.module("tmcApp").controller("AboutCtrl", ["$scope", function(a) {}]), angular.module("tmcApp").controller("BatchCtrl", ["$scope", "tmcalculatorData", "tmcalc", "$routeParams", "$location", "$window", function(a, b, c, d, e, f) {
    a.input = {}, a.result = {}, a.output = [], a.input.p1 = "", a.input.p2 = "", a.input.id1 = "", a.input.id2 = "", a.input.ct = .25, a.result.tm1 = "", a.result.tm2 = "", a.result.ta = "", a.result.itemlist = [], a.result.critlist = [], a.input.groupKeys = [], a.input.products = {}, a.input.prodKeys = [], a.input.group = "", a.input.product = "", a.input.batch = "", a.input.filename = "", a.result.batch = "", a.result.batch2 = "", a.p1status = "", a.p2status = "", b.restoreUserPrefs() ? (a.lastp1 = b.restoreUserPrefs().p1, a.lastp2 = b.restoreUserPrefs().p2) : (a.lastp1 = "", a.lastp2 = "");
    var g = d.p1seq || a.lastp1 || "",
        h = d.p2seq || a.lastp2 || "";
    a.prefill = function() {
        a.input.batch = "P1fwd	AGCGGATAACAATTTCACACAGGA	P1rev	GTAAAACGACGGCCAGT\nP2fwd	AGCGGATAACAATTTCAC	P2rev	GTAAAACGACGGCCA\n", a.output.showresultstable = !1, a.data_toggle_label = a.output.showresultstable ? "Hide" : "Show", a.runCalc3()
    }, a.clearCalc = function() {
        a.input.batch = "", a.input.filename = "", a.output = [], a.result.itemlist = [], a.result.critlist = [], a.result.batch = "", a.result.batch2 = "", a.runmsg = "";
        var b = angular.element("#fileinput");
        b.wrap("<form>").closest("form").get(0).reset(), b.unwrap(), a.output.showresultstable = !1, a.data_toggle_label = a.output.showresultstable ? "Hide" : "Show"
    }, a.setGroups = function() {
        a.input.groupKeys = b.getGroupKeys(), a.input.group = a.input.groupKeys[0]
    }, a.setProducts = function() {
        a.input.group;
        a.input.productKeys = b.getProductKeysForGroup(a.input.group), a.input.products = b.getProductsForGroup(a.input.group), a.input.product = a.input.products[0].id;
        a.input.product;
        a.setCt()
    }, a.setCt = function() {
        var b = a.input.group,
            c = a.input.product;
        0 === b.indexOf("Phusion") || 0 === b.indexOf("Q5") ? a.input.ct = 500 : 0 === b.indexOf("LongAmp") ? a.input.ct = 400 : 0 === b.indexOf("Master") ? 0 === c.indexOf("phusion") || 0 === c.indexOf("q5") ? a.input.ct = 500 : 0 === c.indexOf("lataq") || 0 === c.indexOf("lahstaq") ? a.input.ct = 400 : a.input.ct = 200 : a.input.ct = 200, a.runCalc3()
    }, a.runCalc3 = function() {
        var d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x = a.input.batch,
            y = "",
            z = "",
            A = "",
            B = "",
            C = "",
            D = a.input.ct / 1e3,
            E = a.input.product,
            F = a.input.group,
            G = [],
            H = [],
            I = 0,
            J = /[\t\;]/,
            K = !1,
            L = 1,
            M = 0,
            N = x.split(/\n\r?/);
        a.result = {}, a.output = [], a.ctstatus = "", a.runmsg = "", a.output.showresultstable = !1, a.data_toggle_label = a.output.showresultstable ? "Hide" : "Show";
        for (var O = 0; O < N.length; ++O) N[O].match(/^\s*$/) && N.splice(O, 1);
        if (N.length > 1 && N[0].split(J).length < 4 && (K = !0, L = 2, M = 1), 0 >= D || isNaN(D / 1)) return i = !1, a.ctstatus = "invalidct", H.push("Invalid primer concentration. "), a.result.itemlist = G, a.result.critlist = H, void(a.p1status = "");
        switch (f = b.getBufferIdForProduct(E), "onetaq_gc" === f && (I = 5), g = b.getBufferSaltForProduct(a.input.product), F) {
            case "Phusion":
            case "Phusion Hot Start Flex":
                h = 1;
                break;
            case "Master Mix":
                h = 0 === E.indexOf("phusion") ? 1 : 4;
                break;
            default:
                h = 4
        }
        r = b.validateBuffer(E, F, f), r.hasCritWarnings && Array.prototype.push.apply(H, r.critwarnings), r.hasWarnings && Array.prototype.push.apply(G, r.warnings), a.result.itemlist = G, a.result.critlist = H, c.setCt(D).setSalt(g).setMethod(h).setDMSO(I), k = 0, l = 0, o = 0;
        for (var P = M; P < N.length; P += L) {
            if (C = "OK", m = !1, n = !1, K) {
                if (d = N[P - 1].split(J), e = N[P].split(J), d.length < 2 || e.length < 2) {
                    ++o;
                    continue
                }
                y = d[1], A = d[0], z = e[1], B = e[0]
            } else {
                if (d = N[P].split(J), d.length < 4) {
                    ++o;
                    continue
                }
                y = d[1], z = d[3], A = d[0], B = d[2]
            }
            a.input.p1 = y.toUpperCase(), a.input.p2 = z.toUpperCase(), a.input.id1 = A, a.input.id2 = B, p = b.validateInput(a.input.p1.replace(/\s/g, ""), a.input.p2.replace(/\s/g, ""), D, E, F), s = p.p1isValid, t = p.p2isValid, j = p.hasCritWarnings, a.p1status = p.p1status, a.p2status = p.p2status, j && (C = p.critwarnings.join("-- "), m = !0), "invalidseq" !== a.p1status ? (v = c.Tm(y.replace(/\s/g, "")).tm, v = Math.round(Math.round(10 * v) / 10), a.result.tm1 = v) : a.result.tm1 = "---", "invalidseq" !== a.p2status ? (w = c.Tm(z.replace(/\s/g, "")).tm, w = Math.round(Math.round(10 * w) / 10), a.result.tm2 = w) : a.result.tm2 = "---", "invalidseq" !== a.p1status && "invalidseq" !== a.p2status ? (u = b.getAnnealTemp(y, v, z, w, F, E), a.result.ta = Math.round(u), q = b.validateTm(v, w, u, E, F, f), q.hasCritWarnings && (n = !0, C += "--" + q.critwarnings.join("--")), q.hasWarnings && (n = !0, C += "-- " + q.warnings.join("-- "))) : a.result.ta = "---", m && (k += 1), n && (l += 1), a.output.push([a.input.id1, a.input.p1, a.result.tm1, a.input.id2, a.input.p2, a.result.tm2, a.result.ta, C].join("	")), a.p1status = ""
        }
        a.output.length > 0 && a.output.unshift(["ID 1", "Primer 1 sequence", "Tm 1", "ID 2", "Primer 2 sequence", "Tm 2", "Anneal temp", "Notes"].join("	")), o > 0 ? a.runmsg = o + " Invalid line(s) " : a.runmsg = "", a.runmsg += a.output.length - 1 + " pair(s) processed. Errors: " + k + " Warnings: " + l, a.result.batch = a.output.join("\n"), a.result.batch2 = [];
        for (var Q = 0; Q < a.output.length; ++Q) a.result.batch2.push(a.output[Q].split("	"));
        0 == a.output.length && N.length > 0 ? a.novaliddatamsg = "Unable to detect format or no valid data entered -- check format of 1st line." : a.novaliddatamsg = ""
    }, a.getBatchResults = function() {
        return a.result.batch
    }, a.downloadData = function() {
        var b = a.getBatchResults(),
            c = "tmcalc_batch.txt",
            d = new Blob([b], {
                type: "text/plain;charset=utf-8"
            });
        saveAs(d, c)
    };
    var i = function() {
        return "Product selections and sequence data will not be preserved if you leave this page."
    };
    a.$on("$routeChangeStart", function() {
        i()
    }), a.about = function() {
        e.path("#/about")
    }, a.safeApply = function(a) {
        var b = this.$root.$$phase;
        "$apply" == b || "$digest" == b ? a && "function" == typeof a && a() : this.$apply(a)
    }, a.processFileData = function(b) {
        a.safeApply(function() {
            a.input.batch = b, a.output.showresultstable = !1, a.data_toggle_label = a.output.showresultstable ? "Hide" : "Show", a.runCalc3()
        })
    }, a.switch2single = function() {
        e.path("/")
    }, a.toggle_data_display = function() {
        a.output.showresultstable = !a.output.showresultstable, a.data_toggle_label = a.output.showresultstable ? "Hide" : "Show"
    }, a.output.showresultstable = !1, a.data_toggle_label = a.output.showresultstable ? "Hide" : "Show", a.input.p1 = g, a.input.p2 = h, a.setGroups(), a.setProducts()
}]), angular.module("tmcApp").run(["$templateCache", function(a) {
    a.put("views/about.204cf15b.html", '<div id="one-true" class="row-fluid one-true"> <!-- <div id="sidebar-container" class="col-xs-1 one-true-col dnp">\r\n    </div> --> <div class="col-xs-8 col-xs-offset-1 one-true-col"> <a href="" ng-href="/#!/">Back to Home Page</a> <div class="filler"></div> <div id="aboutdescription" class="row-fluid aboutcontent"> <h4 class="orange">NEB Tm Calculator v{{appVersion}}</h4> <p>The NEB Tm calculator is intended for use in estimating the optimal annealing temperature for PCR with NEB polymerases. </p> <h4 class="orange">System Requirements</h4> <p>NEB Tm Calculator is best used on modern web browsers that are compliant with HTML5 and CSS3 standards. Javascript must be enabled for the tool to work. </p> <h4 class="orange">Privacy</h4> <p>NEB Tm Calculator does not store or transfer any user data to NEB servers. All calculations are handled within the user\'s browser. NEB Tm Calculator incorporates code from Google Analytics, which may transmit anonymous usage data (page access numbers and times, user IP, user browser version, etc.) to Google. </p> <h4 class="orange">Legal</h4> <p> <a href="https://www.neb.com/trademarks">Trademark information</a>. </p> <p> <a href="https://www.neb.com/patents">Patent information</a>. </p> <p> <a href="https://www.neb.com/about-neb/business-development-opportunities">Licensing information</a>. </p> </div> </div><!-- .content --> </div>'), a.put("views/batch.03c23ef3.html", '<div id="one-true" class="row one-true"> <div id="sidebar-container" class="col-sm-3 one-true-col dnp"> <div ng-include="\'views/batchsidebar.23048bea.html\'"></div> </div> <div class="col-sm-9 one-true-col"> <div class="row content"> <div id="input" class="col-sm-12"> <div class="row"> <!-- <div class="blue explain" ng-click="openmodal(\'tmchangenote\', \'md\')">Note: Recent changes to Tm calculations</div> --> <div class="col-sm-8"> <span class="fieldlabel">Product Group</span><br> <select ng-model="input.group" ng-options="gr for gr in input.groupKeys" ng-change="setProducts()"> <!-- <option ng-repeat="gr in input.groupKeys" value="{{gr}}">{{gr}}</option> --> </select><br> <span class="fieldlabel">Polymerase/Kit</span><br> <select ng-model="input.product" ng-options="pr.id as pr.name for pr in input.products" ng-change="setCt()"> <!-- <option ng-repeat="pr in input.productKeys" value="{{pr}}">{{pr}}</option> --> </select><br> </div> </div> <div class="row"> <div class="col-sm-8"> <div class="row"> <div class="col-sm-7"> <span class="fieldlabel">Primer Concentration (nM)</span><br> <input id="ct" ng-class="ctstatus" ng-model="input.ct" type="number" required ng-change="runCalc2()"> </div> <div class="col-sm-5"> <div class="dnp refresh-holder"> <span class="glyphicon glyphicon-refresh"></span> <a class="btn-link" ng-click="setCt()">Reset concentration </a> </div> </div> </div> </div> </div> <br> <div class="row"> <div class="col-sm-12"> <span class="fieldlabel">Primer Pairs</span><br> <textarea id="batchinput" ng-model="input.batch" ng-class="p1status" ng-change="runCalc3()" placeholder="ID#1 ; Primer1 ; ID#2 ; Primer2 -newline-">\r\n                        </textarea> <div id="fileinputcontainer"> <span>Load primer pairs from file: </span> <input type="file" fileinput processwith="processFileData(filedata)" ng-model="input.filename" id="fileinput"> </div> </div> </div> <div class="row"> <div class="col-sm-8"> <div class="row"> <div class="col-sm-7"> <a ng-click="switch2single()" class="btn-link dnp">Switch to single pair mode</a> </div> <div class="col-sm-5"> <a ng-click="clearCalc()" class="btn-link dnp">Clear</a> <br> <a ng-click="prefill()" class="btn-link dnp">Use example input</a> <br> </div> </div> </div> </div> <div class="row"> <div class="col-sm-12"> <div id="result" class="col-sm-12" ng-hide="output"> <span class="invalidseq">{{novaliddatamsg}}</span> </div> </div> </div> <div class="row"> <div class="col-sm-12"> <div id="result" ng-show="output.length"> <a ng-click="toggle_data_display()" class="btn-link dnp">{{data_toggle_label}} results</a> <a class="downloadfile" href="" ng-click="downloadData()"> <img ng-src="images/download3i.d680661d.png"> </a> <br> <div ng-hide="output.showresultstable"><h4>{{runmsg}}</h4></div> <table class="batchresultstable" ng-show="output.showresultstable"> <tr ng-repeat="row in result.batch2"> <td ng-repeat="idx in [0,1,2,3,4,5,6,7]" class="batchresultscell">{{row[idx]}}</td> </tr> </table> </div> </div> </div> </div> </div> <div class="row"> <div class="col-sm-11"> <hr> <div id="crit" class="notes"> <ul> <li ng-repeat="item in result.critlist">{{item}}</li> </ul> </div> <div id="warn" class="notes" ng-show="result.ta"> <ul> <li ng-repeat="item in result.itemlist">{{item}}</li> </ul> </div> </div> </div> </div> </div>'), a.put("views/batchsidebar.23048bea.html", '<div id="sidemenu" class="sidemenu"> <button id="toggle-sidebar" class="btn-link visible-phone" data-toggle="collapse" data-target="#sidebar-content"> <!-- <span class="icon-th-list"></span> --> <i class="icon-chevron-down"></i> </button> <div id="idebar-content" class="collapse in"> <p> Use the NEB Tm Calculator to estimate an appropriate annealing temperature when using NEB PCR products. </p><p> <strong>Instructions</strong> <ol> <li>Select the product group of the polymerase or kit you plan to use.</li> <li>Select the polymerase or kit from the list of products.</li> <li>If needed, modify the recommended primer concentration.</li> <li>Enter primer sequence pairs (ACGT only). Spaces allowed. Primer pairs (one pair per line) are expected to be in the format ID1 Primer1 ID2 Primer2, with values separated by semicolons. Data loaded from a plain text file or by copy/paste may also use tabs. </li> </ol> </p><p> Results can be downloaded in tab-delimited format as a plain text file in many modern browsers. In some browsers, file download will trigger display of the output in a new tab. <strong>Input lines that do not match the expected format are ignored.</strong> Please visit <a href="" ng-href="/#!/help">Help</a> for more information. </p> </div> </div>'), a.put("views/help.ef501d45.html", '<div id="one-true" class="row-fluid one-true"> <!-- <div id="sidebar-container" class="col-xs-1 one-true-col dnp">\r\n    </div> --> <div class="col-xs-8 col-xs-offset-1 one-true-col"> <a href="" ng-href="/#!/">Back to Home Page</a> <div class="filler"></div> <div id="helpdescription" class="row-fluid helpcontent"> <h4 class="orange">Help</h4> <p> The NEB Tm calculator is intended for use in estimating the optimal annealing temperature for PCR with NEB polymerases. Tm values are calculated using thermodynamic data from Santa Lucia [1] and the salt correction of Owczarzy [2]. For Phusion® DNA Polymerases, the thermodynamic data is from Breslauer et al. [3] and uses the salt correction of Schildkraut [2]. </p> <h4 class="orange">Batch Processing</h4> <p> In batch mode, the NEB Tm calculator will process multiple pairs of primer sequences and provide a tabular output. Primer pairs may be entered directly into the text box, copied and pasted into the text box, or loaded from a local file. In many modern browsers, a file can be dropped onto the file selection/browse button from the desktop. After processing, results may be downloaded in tab-delimited format as a plain text file. In some browsers (including Safari), file download will trigger display of the output in a new tab. The data may be copied from that tab or saved using the browser\'s <b>File Save As ...</b> menu function. Copy-to-clipboard functionality has been disabled as it relied on Flash plugins that are being blocked by many modern browsers. <strong>Note that input lines that do not match the expected format (see below) or have just a single sequence are skipped and not shown in the output.</strong> Errors and warnings are listed and attached to each line in the output. The output is best viewed by pasting it into a spreadsheet. </p> <p> Primer pairs (one pair per line) are expected to be in the following format: </p> <p> <em><strong>ID1</strong> [separator] <strong>Primer1 sequence</strong> [separator] <strong>ID2</strong> [separator] <strong>Primer2 sequence</strong></em> </p> <p> <tt> P1fwd AGCGGATAACAATTTCACACAGGA P1rev GTAAAACGACGGCCAGT <br> P1fwd; AGCGGATAACAATTTCACACAGGA; P1rev; GTAAAACGACGGCCAGT </tt> </p> <p> where the separators can be tabs or semicolons. Tab-separated (tsv) or semicolon-separated data exported from Microsoft Excel spreadsheets is acceptable. CSV (comma-separated files) will not work. The primer sequence must contain only A,C,G,T or spaces. <strong>Please note that tabs cannot be entered directly into the text area, so manual entry should use semicolons as separators. </strong> If the first input line contains only one primer, the data is assumed to be interleaved, with primer pairs split over subsequent lines. The entire input file must use the same format for input. </p> <h4 class="orange">How do I calculate just the Tm for a list of sequences (not pairs)?</h4> <p> The NEB Tm calculator is designed to recommend optimal annealing temperatures for primer pairs. To get Tm values for a list of single primers, enter them one per line (ID1; Sequence1) but append ;; (2 semicolons) after the primer sequence. The software will process the line as having an invalid second primer, but will calculate the Tm of the first primer. </p> <h4 class="orange">Why is the primer Tm (or annealing temperature) different from other Tm calculators?</h4> <p> The NEB Tm calculator is designed to take into account the buffer conditions of the amplification reaction based on the selected NEB polymerase. Many Tm calculators do not, relying instead on a default salt concentration. The annealing temperature for each polymerase is based on empirical observations of efficiency. The optimal annealing temperature for high fidelity hot start DNA polymerases like Q5 may differ significantly from that of Taq-based polymerases. </p> <h4 class="orange">Tm Calculation Method</h4> <p> The general format for `T_m` calculation is </p> <p style="text-align:center"> `T_m = (\\DeltaH^o)/(\\DeltaS^o + R * ln C_p) - 273.15` </p> <p> where `C_p` is the primer concentration, `DeltaH^o` is enthalpy (`cal*mol^-1`), `\\DeltaS^o` is entropy (`cal*K^-1*mol^-1`) and `R` is the universal gas constant (1.987`cal*K^-1*mol^-1`). `DeltaH^o` and `\\DeltaS^o` are computed from experimentally derived values for these parameters using the nearest-neighbor model, summing over all dinucleotides in the primer sequence. 273.15 is subtracted to convert from Kelvin to Celsius. </p> <p> In the NEB Tm Calculator, `T_m` is computed by the method of SantaLucia [1] as </p> <p style="text-align:center"> `T_m = ((\\DeltaH_i^o + \\DeltaH^o) * 1000)/(\\DeltaS_i^o + \\DeltaS^o + R * ln C_p) - 273.15` </p> <p> where the primer concentration `C_p` is assumed to be significantly greater (6x) than the target template concentration. `DeltaH^o` and `\\DeltaS^o` are computed using the nearest-neighbor model values outlined in [1]. `DeltaH_i^o` and `\\DeltaS_i^o` are adjustments for helix initiation [1]. The factor of 1000 is included to convert enthalpy values reported in `kcal*mol^-1` to `cal*mol^-1`. </p> <p> The `T_m`, as calculated above, assumes a 1 M monovalent cation concentration. This value is adjusted to reaction buffer conditions using the salt correction of Owczarzy as outlined in [2] </p> <p style="text-align:center"> `T_m` (corrected) `= 1 / (1 / T_m + [(4.29 * f_{gc} - 3.95) * ln(m) + 0.94 * (ln(m))^2] * 10^-5)` </p> <p> where `f_{gc}` is the fractional GC content, and `m` is the monovalent cation concentration. </p> <p> For Phusion® polymerases, `T_m` is computed by the method of Breslauer [3] as </p> <p style="text-align:center"> `T_m = ((\\DeltaH^o) * 1000)/(\\DeltaS_i^o + \\DeltaS^o + R * ln (C_p/4)) - 273.15` </p> <p> `DeltaH^o` and `\\DeltaS^o` are computed using the nearest-neighbor model values published in [3]. `\\DeltaS_i^o` is an adjustment for helix initiation [3]. The factor of 1000 is included to convert enthalpy values reported in `kcal*mol^-1` to `cal*mol^-1`. </p> <p> The `T_m` is adjusted to reaction buffer conditions using the salt correction of Schildkraut as outlined in [2] </p> <p style="text-align:center"> `T_m` (corrected) `= T_m + 16.6 * ln(m)` </p> <p> where `m` is the monovalent cation concentration. </p> <p> While the method and data of SantaLucia are preferred, it was necessary to use the Breslauer data and modified equations for annealing temperatures in reactions using Phusion® polymerases to allow compatibility with recommendations provided by Finnzymes Oy, now a part of Thermo Fisher Scientific. </p> <hr> <p> <small> <ol> <li>SantaLucia (1998) PNAS 95:1460-5</li> <li>Owczarzy et al (2004) Biochem 43:3537-54</li> <li>Breslauer et al (1986) Proc. Nat. Acad. Sci. 83:3746-50</li> </ol> </small> </p> </div> </div> </div> <script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=AM_HTMLorMML-full"></script>'),
        a.put("views/main.9b69837c.html", '<div id="one-true" class="row one-true"> <div id="sidebar-container" class="col-sm-3 one-true-col dnp"> <div ng-include="\'views/sidebar.7a38702b.html\'"></div> </div> <div class="col-sm-9 one-true-col"> <div class="row content"> <div id="input" class="col-sm-8"> <div class="row"> <!-- <span class="blue explain" ng-click="openmodal(\'tmchangenote\', \'md\')">Note: Recent changes to Tm calculations</span> --> <div class="col-sm-12"> <span class="fieldlabel">Product Group</span><br> <select ng-model="input.group" ng-options="gr for gr in input.groupKeys" ng-change="setProducts()"> <!-- <option ng-repeat="gr in input.groupKeys" value="{{gr}}">{{gr}}</option> --> </select><br> <span class="fieldlabel">Polymerase/Kit</span><br> <select ng-model="input.product" ng-options="pr.id as pr.name for pr in input.products" ng-change="setCt()"> <!-- <option ng-repeat="pr in input.productKeys" value="{{pr}}">{{pr}}</option> --> </select><br> </div> </div> <div class="row"> <div class="col-sm-7"> <span class="fieldlabel">Primer Concentration (nM)</span><br> <input id="ct" ng-class="ctstatus" ng-model="input.ct" type="number" required ng-change="runCalc2()"> </div> <div class="col-sm-5"> <div class="dnp refresh-holder"> <span class="glyphicon glyphicon-refresh"></span> <a class="btn-link" ng-click="setCt()">Reset concentration </a> </div> </div> </div> <div class="row"> <div class="col-sm-12"> <span class="fieldlabel">Primer 1</span><br> <input id="p1" ng-model="input.p1" type="text" ng-class="p1status" ng-change="runCalc2()" placeholder="Primer 1 Sequence"> <span class="fieldlabel">Primer 2</span><br> <input id="p2" ng-model="input.p2" type="text" ng-class="p2status" ng-change="runCalc2()" placeholder="Primer 2 Sequence"> </div> </div> <br> <div class="row"> <div class="col-sm-7"> <a ng-click="switch2batch()" class="btn-link dnp">Switch to batch mode</a> </div> <div class="col-sm-5"> <a ng-click="clearCalc()" class="btn-link dnp">Clear</a> <br> <a ng-click="prefill()" class="btn-link dnp">Use example input</a> <br> </div> </div> </div> <div id="result" class="col-sm-4"> <div id="ta" class="answer" ng-show="result.ta"> <strong>Anneal at</strong><br> <h2>{{result.ta}} &deg;C</h2> </div> <div id="tm1" class="answer"> <div class="tiny-label">Primer 1</div> <div ng-show="result.tm1"> <strong>{{result.len1}} nt</strong><br> <strong>{{result.gc1}}% GC</strong><br> <strong>Tm: {{result.tm1}} &deg;C</strong> </div> </div> <div id="tm2" class="answer"> <div class="tiny-label">Primer 2</div> <div ng-show="result.tm2"> <strong>{{result.len2}} nt</strong><br> <strong>{{result.gc2}}% GC</strong><br> <strong>Tm: {{result.tm2}} &deg;C</strong> </div> </div> </div> </div> <!-- <div class="container-fluid"> --> <div class="row"> <div class="col-sm-8"> <hr> <div id="crit" class="notes"> <ul> <li ng-repeat="item in result.critlist">{{item}}</li> </ul> </div> <div id="warn" class="notes" ng-show="result.ta"> <ul> <li ng-repeat="item in result.itemlist">{{item}}</li> </ul> </div> </div> </div> <!-- </div> --> </div> </div> '), a.put("views/modals/tmchangenote.html", '<div class="modal-header"> <h4 class="modal-title">Recent changes to Tm calculations</h4> </div> <div class="modal-body"> <p> The calculations in the NEB Tm calculator were recently modified to correct an error that was decreasing the effective primer concentration to one quarter of it\'s input value. The correction raises Tm values by roughly 2&deg;C for all polymerase reaction buffers except Phusion, which uses a different algorithm. The recommended annealing temperature for reactions using Q5 polymerases has been adjusted, and reported values will be nearly the same as before the correction. The values for Taq-related polymerases were not adjusted, as the broad activity profile for these enzymes accommodates the changes without detrimental effects to yield. Please contact NEB technical support if you need additional guidance. </p> </div> <div class="modal-footer"> <button class="btn orange-btn" ng-click="modalOptions.ok()">OK</button> </div>'), a.put("views/sidebar.7a38702b.html", '<div id="sidemenu" class="sidemenu"> <button id="toggle-sidebar" class="btn-link visible-phone" data-toggle="collapse" data-target="#sidebar-content"> <!-- <span class="icon-th-list"></span> --> <i class="icon-chevron-down"></i> </button> <div id="sidebar-content" class="collapse in"> <p> Use the NEB Tm Calculator to estimate an appropriate annealing temperature when using NEB PCR products. </p><p> <strong>Instructions</strong> <ol> <li>Select the product group of the polymerase or kit you plan to use.</li> <li>Select the polymerase or kit from the list of products.</li> <li>If needed, modify the recommended primer concentration.</li> <li>Enter primer sequences (ACGT only) that anneal to the template. Spaces allowed. </li> </ol> </p><p> Note that an anealing temperature will only be displayed if both primer sequences are entered. </p> </div> </div>')
}]);
