(function(e) { (function() {
        function h(i, s, u, f, c, h, p, d, v, m, g, y, b, w, E, S) {
            if (s || t === -1) {
                e.expressions[++t] = [],
                n = -1;
                if (s) return ""
            }
            if (u || f || n === -1) {
                u = u || " ";
                var x = e.expressions[t];
                r && x[n] && (x[n].reverseCombinator = a(u)),
                x[++n] = {
                    combinator: u,
                    tag: "*"
                }
            }
            var T = e.expressions[t][n];
            if (c) T.tag = c.replace(o, "");
            else if (h) T.id = h.replace(o, "");
            else if (p) p = p.replace(o, ""),
            T.classList || (T.classList = []),
            T.classes || (T.classes = []),
            T.classList.push(p),
            T.classes.push({
                value: p,
                regexp: new RegExp("(^|\\s)" + l(p) + "(\\s|$)")
            });
            else if (b) S = S || E,
            S = S ? S.replace(o, "") : null,
            T.pseudos || (T.pseudos = []),
            T.pseudos.push({
                key: b.replace(o, ""),
                value: S,
                type: y.length == 1 ? "class": "element"
            });
            else if (d) {
                d = d.replace(o, ""),
                g = (g || "").replace(o, "");
                var N, C;
                switch (v) {
                case "^=":
                    C = new RegExp("^" + l(g));
                    break;
                case "$=":
                    C = new RegExp(l(g) + "$");
                    break;
                case "~=":
                    C = new RegExp("(^|\\s)" + l(g) + "(\\s|$)");
                    break;
                case "|=":
                    C = new RegExp("^" + l(g) + "(-|$)");
                    break;
                case "=":
                    N = function(e) {
                        return g == e
                    };
                    break;
                case "*=":
                    N = function(e) {
                        return e && e.indexOf(g) > -1
                    };
                    break;
                case "!=":
                    N = function(e) {
                        return g != e
                    };
                    break;
                default:
                    N = function(e) {
                        return !! e
                    }
                }
                g == "" && /^[*$^]=$/.test(v) && (N = function() {
                    return ! 1
                }),
                N || (N = function(e) {
                    return e && C.test(e)
                }),
                T.attributes || (T.attributes = []),
                T.attributes.push({
                    key: d,
                    operator: v,
                    value: g,
                    test: N
                })
            }
            return ""
        }
        var e, t, n, r, i = {},
        s = {},
        o = /\\/g,
        u = function(n, o) {
            if (n == null) return null;
            if (n.Slick === !0) return n;
            n = ("" + n).replace(/^\s+|\s+$/g, ""),
            r = !!o;
            var a = r ? s: i;
            if (a[n]) return a[n];
            e = {
                Slick: !0,
                expressions: [],
                raw: n,
                reverse: function() {
                    return u(this.raw, !0)
                }
            },
            t = -1;
            while (n != (n = n.replace(c, h)));
            return e.length = e.expressions.length,
            a[e.raw] = r ? f(e) : e
        },
        a = function(e) {
            return e === "!" ? " ": e === " " ? "!": /^!/.test(e) ? e.replace(/^!/, "") : "!" + e
        },
        f = function(e) {
            var t = e.expressions;
            for (var n = 0; n < t.length; n++) {
                var r = t[n],
                i = {
                    parts: [],
                    tag: "*",
                    combinator: a(r[0].combinator)
                };
                for (var s = 0; s < r.length; s++) {
                    var o = r[s];
                    o.reverseCombinator || (o.reverseCombinator = " "),
                    o.combinator = o.reverseCombinator,
                    delete o.reverseCombinator
                }
                r.reverse().push(i)
            }
            return e
        },
        l = function(e) {
            return e.replace(/[-[\]{}()*+?.\\^$|,#\s]/g,
            function(e) {
                return "\\" + e
            })
        },
        c = new RegExp("^(?:\\s*(,)\\s*|\\s*(<combinator>+)\\s*|(\\s+)|(<unicode>+|\\*)|\\#(<unicode>+)|\\.(<unicode>+)|\\[\\s*(<unicode1>+)(?:\\s*([*^$!~|]?=)(?:\\s*(?:([\"']?)(.*?)\\9)))?\\s*\\](?!\\])|(:+)(<unicode>+)(?:\\((?:(?:([\"'])([^\\13]*)\\13)|((?:\\([^)]+\\)|[^()]*)+))\\))?)".replace(/<combinator>/, "[" + l(">+~`!@$%^&={}\\;</") + "]").replace(/<unicode>/g, "(?:[\\w\\u00a1-\\uFFFF-]|\\\\[^\\s0-9a-f])").replace(/<unicode1>/g, "(?:[:\\w\\u00a1-\\uFFFF-]|\\\\[^\\s0-9a-f])")),
        p = this.Slick || {};
        p.parse = function(e) {
            return u(e)
        },
        p.escapeRegExp = l,
        this.Slick || (this.Slick = p)
    }).apply(typeof exports != "undefined" ? exports: this),
    function() {
        var e = {},
        t = {},
        n = Object.prototype.toString;
        e.isNativeCode = function(e) {
            return /\{\s*\[native code\]\s*\}/.test("" + e)
        },
        e.isXML = function(e) {
            return !! e.xmlVersion || !!e.xml || n.call(e) == "[object XMLDocument]" || e.nodeType == 9 && e.documentElement.nodeName != "HTML"
        },
        e.setDocument = function(e) {
            var n = e.nodeType;
            if (n != 9) if (n) e = e.ownerDocument;
            else {
                if (!e.navigator) return;
                e = e.document
            }
            if (this.document === e) return;
            this.document = e;
            var r = e.documentElement,
            i = this.getUIDXML(r),
            s = t[i],
            o;
            if (s) {
                for (o in s) this[o] = s[o];
                return
            }
            s = t[i] = {},
            s.root = r,
            s.isXMLDocument = this.isXML(e),
            s.brokenStarGEBTN = s.starSelectsClosedQSA = s.idGetsName = s.brokenMixedCaseQSA = s.brokenGEBCN = s.brokenCheckedQSA = s.brokenEmptyAttributeQSA = s.isHTMLDocument = s.nativeMatchesSelector = !1;
            var u, a, f, l, c, h, p = "slick_uniqueid",
            d = e.createElement("div"),
            v = e.body || e.getElementsByTagName("body")[0] || r;
            v.appendChild(d);
            try {
                d.innerHTML = '<a id="' + p + '"></a>',
                s.isHTMLDocument = !!e.getElementById(p)
            } catch(m) {}
            if (s.isHTMLDocument) {
                d.style.display = "none",
                d.appendChild(e.createComment("")),
                a = d.getElementsByTagName("*").length > 1;
                try {
                    d.innerHTML = "foo</foo>",
                    h = d.getElementsByTagName("*"),
                    u = h && !!h.length && h[0].nodeName.charAt(0) == "/"
                } catch(m) {}
                s.brokenStarGEBTN = a || u;
                try {
                    d.innerHTML = '<a name="' + p + '"></a><b id="' + p + '"></b>',
                    s.idGetsName = e.getElementById(p) === d.firstChild
                } catch(m) {}
                if (d.getElementsByClassName) {
                    try {
                        d.innerHTML = '<a class="f"></a><a class="b"></a>',
                        d.getElementsByClassName("b").length,
                        d.firstChild.className = "b",
                        l = d.getElementsByClassName("b").length != 2
                    } catch(m) {}
                    try {
                        d.innerHTML = '<a class="a"></a><a class="f b a"></a>',
                        f = d.getElementsByClassName("a").length != 2
                    } catch(m) {}
                    s.brokenGEBCN = l || f
                }
                if (d.querySelectorAll) {
                    try {
                        d.innerHTML = "foo</foo>",
                        h = d.querySelectorAll("*"),
                        s.starSelectsClosedQSA = h && !!h.length && h[0].nodeName.charAt(0) == "/"
                    } catch(m) {}
                    try {
                        d.innerHTML = '<a class="MiX"></a>',
                        s.brokenMixedCaseQSA = !d.querySelectorAll(".MiX").length
                    } catch(m) {}
                    try {
                        d.innerHTML = '<select><option selected="selected">a</option></select>',
                        s.brokenCheckedQSA = d.querySelectorAll(":checked").length == 0
                    } catch(m) {}
                    try {
                        d.innerHTML = '<a class=""></a>',
                        s.brokenEmptyAttributeQSA = d.querySelectorAll('[class*=""]').length != 0
                    } catch(m) {}
                }
                try {
                    d.innerHTML = '<form action="s"><input id="action"/></form>',
                    c = d.firstChild.getAttribute("action") != "s"
                } catch(m) {}
                s.nativeMatchesSelector = r.matchesSelector || r.mozMatchesSelector || r.webkitMatchesSelector;
                if (s.nativeMatchesSelector) try {
                    s.nativeMatchesSelector.call(r, ":slick"),
                    s.nativeMatchesSelector = null
                } catch(m) {}
            }
            try {
                r.slick_expando = 1,
                delete r.slick_expando,
                s.getUID = this.getUIDHTML
            } catch(m) {
                s.getUID = this.getUIDXML
            }
            v.removeChild(d),
            d = h = v = null,
            s.getAttribute = s.isHTMLDocument && c ?
            function(e, t) {
                var n = this.attributeGetters[t];
                if (n) return n.call(e);
                var r = e.getAttributeNode(t);
                return r ? r.nodeValue: null
            }: function(e, t) {
                var n = this.attributeGetters[t];
                return n ? n.call(e) : e.getAttribute(t)
            },
            s.hasAttribute = r && this.isNativeCode(r.hasAttribute) ?
            function(e, t) {
                return e.hasAttribute(t)
            }: function(e, t) {
                return e = e.getAttributeNode(t),
                !(!e || !e.specified && !e.nodeValue)
            },
            s.contains = r && this.isNativeCode(r.contains) ?
            function(e, t) {
                return e.contains(t)
            }: r && r.compareDocumentPosition ?
            function(e, t) {
                return e === t || !!(e.compareDocumentPosition(t) & 16)
            }: function(e, t) {
                if (t) do
                if (t === e) return ! 0;
                while (t = t.parentNode);
                return ! 1
            },
            s.documentSorter = r.compareDocumentPosition ?
            function(e, t) {
                return ! e.compareDocumentPosition || !t.compareDocumentPosition ? 0 : e.compareDocumentPosition(t) & 4 ? -1 : e === t ? 0 : 1
            }: "sourceIndex" in r ?
            function(e, t) {
                return ! e.sourceIndex || !t.sourceIndex ? 0 : e.sourceIndex - t.sourceIndex
            }: e.createRange ?
            function(e, t) {
                if (!e.ownerDocument || !t.ownerDocument) return 0;
                var n = e.ownerDocument.createRange(),
                r = t.ownerDocument.createRange();
                return n.setStart(e, 0),
                n.setEnd(e, 0),
                r.setStart(t, 0),
                r.setEnd(t, 0),
                n.compareBoundaryPoints(Range.START_TO_END, r)
            }: null,
            r = null;
            for (o in s) this[o] = s[o]
        };
        var r = /^([#.]?)((?:[\w-]+|\*))$/,
        i = /\[.+[*$^]=(?:""|'')?\]/,
        s = {};
        e.search = function(e, t, n, o) {
            var u = this.found = o ? null: n || [];
            if (!e) return u;
            if (e.navigator) e = e.document;
            else if (!e.nodeType) return u;
            var a, f, l = this.uniques = {},
            h = !!n && !!n.length,
            p = e.nodeType == 9;
            this.document !== (p ? e: e.ownerDocument) && this.setDocument(e);
            if (h) for (f = u.length; f--;) l[this.getUID(u[f])] = !0;
            if (typeof t == "string") {
                var d = t.match(r);
                e: if (d) {
                    var v = d[1],
                    m = d[2],
                    g,
                    y;
                    if (!v) {
                        if (m == "*" && this.brokenStarGEBTN) break e;
                        y = e.getElementsByTagName(m);
                        if (o) return y[0] || null;
                        for (f = 0; g = y[f++];)(!h || !l[this.getUID(g)]) && u.push(g)
                    } else if (v == "#") {
                        if (!this.isHTMLDocument || !p) break e;
                        g = e.getElementById(m);
                        if (!g) return u;
                        if (this.idGetsName && g.getAttributeNode("id").nodeValue != m) break e;
                        if (o) return g || null; (!h || !l[this.getUID(g)]) && u.push(g)
                    } else if (v == ".") {
                        if (!this.isHTMLDocument || (!e.getElementsByClassName || this.brokenGEBCN) && e.querySelectorAll) break e;
                        if (e.getElementsByClassName && !this.brokenGEBCN) {
                            y = e.getElementsByClassName(m);
                            if (o) return y[0] || null;
                            for (f = 0; g = y[f++];)(!h || !l[this.getUID(g)]) && u.push(g)
                        } else {
                            var b = new RegExp("(^|\\s)" + c.escapeRegExp(m) + "(\\s|$)");
                            y = e.getElementsByTagName("*");
                            for (f = 0; g = y[f++];) {
                                className = g.className;
                                if (!className || !b.test(className)) continue;
                                if (o) return g; (!h || !l[this.getUID(g)]) && u.push(g)
                            }
                        }
                    }
                    return h && this.sort(u),
                    o ? null: u
                }
                t: if (e.querySelectorAll) {
                    if (!this.isHTMLDocument || s[t] || this.brokenMixedCaseQSA || this.brokenCheckedQSA && t.indexOf(":checked") > -1 || this.brokenEmptyAttributeQSA && i.test(t) || !p && t.indexOf(",") > -1 || c.disableQSA) break t;
                    var w = t,
                    E = e;
                    if (!p) {
                        var S = E.getAttribute("id"),
                        x = "slickid__";
                        E.setAttribute("id", x),
                        w = "#" + x + " " + w,
                        e = E.parentNode
                    }
                    try {
                        if (o) return e.querySelector(w) || null;
                        y = e.querySelectorAll(w)
                    } catch(T) {
                        s[t] = 1;
                        break t
                    } finally {
                        p || (S ? E.setAttribute("id", S) : E.removeAttribute("id"), e = E)
                    }
                    if (this.starSelectsClosedQSA) for (f = 0; g = y[f++];) g.nodeName > "@" && (!h || !l[this.getUID(g)]) && u.push(g);
                    else for (f = 0; g = y[f++];)(!h || !l[this.getUID(g)]) && u.push(g);
                    return h && this.sort(u),
                    u
                }
                a = this.Slick.parse(t);
                if (!a.length) return u
            } else {
                if (t == null) return u;
                if (!t.Slick) return this.contains(e.documentElement || e, t) ? (u ? u.push(t) : u = t, u) : u;
                a = t
            }
            this.posNTH = {},
            this.posNTHLast = {},
            this.posNTHType = {},
            this.posNTHTypeLast = {},
            this.push = !h && (o || a.length == 1 && a.expressions[0].length == 1) ? this.pushArray: this.pushUID,
            u == null && (u = []);
            var N, C, k, L, A, O, M, _, D, P, H, B, j, F, I = a.expressions;
            n: for (f = 0; B = I[f]; f++) for (N = 0; j = B[N]; N++) {
                L = "combinator:" + j.combinator;
                if (!this[L]) continue n;
                A = this.isXMLDocument ? j.tag: j.tag.toUpperCase(),
                O = j.id,
                M = j.classList,
                _ = j.classes,
                D = j.attributes,
                P = j.pseudos,
                F = N === B.length - 1,
                this.bitUniques = {},
                F ? (this.uniques = l, this.found = u) : (this.uniques = {},
                this.found = []);
                if (N === 0) {
                    this[L](e, A, O, _, D, P, M);
                    if (o && F && u.length) break n
                } else if (o && F) for (C = 0, k = H.length; C < k; C++) {
                    this[L](H[C], A, O, _, D, P, M);
                    if (u.length) break n
                } else for (C = 0, k = H.length; C < k; C++) this[L](H[C], A, O, _, D, P, M);
                H = this.found
            }
            return (h || a.expressions.length > 1) && this.sort(u),
            o ? u[0] || null: u
        },
        e.uidx = 1,
        e.uidk = "slick-uniqueid",
        e.getUIDXML = function(e) {
            var t = e.getAttribute(this.uidk);
            return t || (t = this.uidx++, e.setAttribute(this.uidk, t)),
            t
        },
        e.getUIDHTML = function(e) {
            return e.uniqueNumber || (e.uniqueNumber = this.uidx++)
        },
        e.sort = function(e) {
            return this.documentSorter ? (e.sort(this.documentSorter), e) : e
        },
        e.cacheNTH = {},
        e.matchNTH = /^([+-]?\d*)?([a-z]+)?([+-]\d+)?$/,
        e.parseNTHArgument = function(e) {
            var t = e.match(this.matchNTH);
            if (!t) return ! 1;
            var n = t[2] || !1,
            r = t[1] || 1;
            r == "-" && (r = -1);
            var i = +t[3] || 0;
            return t = n == "n" ? {
                a: r,
                b: i
            }: n == "odd" ? {
                a: 2,
                b: 1
            }: n == "even" ? {
                a: 2,
                b: 0
            }: {
                a: 0,
                b: r
            },
            this.cacheNTH[e] = t
        },
        e.createNTHPseudo = function(e, t, n, r) {
            return function(i, s) {
                var o = this.getUID(i);
                if (!this[n][o]) {
                    var u = i.parentNode;
                    if (!u) return ! 1;
                    var a = u[e],
                    f = 1;
                    if (r) {
                        var l = i.nodeName;
                        do {
                            if (a.nodeName != l) continue;
                            this[n][this.getUID(a)] = f++
                        } while ( a = a [ t ])
                    } else do {
                        if (a.nodeType != 1) continue;
                        this[n][this.getUID(a)] = f++
                    } while ( a = a [ t ])
                }
                s = s || "n";
                var c = this.cacheNTH[s] || this.parseNTHArgument(s);
                if (!c) return ! 1;
                var h = c.a,
                p = c.b,
                d = this[n][o];
                if (h == 0) return p == d;
                if (h > 0) {
                    if (d < p) return ! 1
                } else if (p < d) return ! 1;
                return (d - p) % h == 0
            }
        },
        e.pushArray = function(e, t, n, r, i, s) {
            this.matchSelector(e, t, n, r, i, s) && this.found.push(e)
        },
        e.pushUID = function(e, t, n, r, i, s) {
            var o = this.getUID(e); ! this.uniques[o] && this.matchSelector(e, t, n, r, i, s) && (this.uniques[o] = !0, this.found.push(e))
        },
        e.matchNode = function(e, t) {
            if (this.isHTMLDocument && this.nativeMatchesSelector) try {
                return this.nativeMatchesSelector.call(e, t.replace(/\[([^=]+)=\s*([^'"\]]+?)\s*\]/g, '[$1="$2"]'))
            } catch(n) {}
            var r = this.Slick.parse(t);
            if (!r) return ! 0;
            var i = r.expressions,
            s = 0,
            o;
            for (o = 0; currentExpression = i[o]; o++) if (currentExpression.length == 1) {
                var u = currentExpression[0];
                if (this.matchSelector(e, this.isXMLDocument ? u.tag: u.tag.toUpperCase(), u.id, u.classes, u.attributes, u.pseudos)) return ! 0;
                s++
            }
            if (s == r.length) return ! 1;
            var a = this.search(this.document, r),
            f;
            for (o = 0; f = a[o++];) if (f === e) return ! 0;
            return ! 1
        },
        e.matchPseudo = function(e, t, n) {
            var r = "pseudo:" + t;
            if (this[r]) return this[r](e, n);
            var i = this.getAttribute(e, t);
            return n ? n == i: !!i
        },
        e.matchSelector = function(e, t, n, r, i, s) {
            if (t) {
                var o = this.isXMLDocument ? e.nodeName: e.nodeName.toUpperCase();
                if (t == "*") {
                    if (o < "@") return ! 1
                } else if (o != t) return ! 1
            }
            if (n && e.getAttribute("id") != n) return ! 1;
            var u, a, f;
            if (r) for (u = r.length; u--;) {
                f = e.getAttribute("class") || e.className;
                if (!f || !r[u].regexp.test(f)) return ! 1
            }
            if (i) for (u = i.length; u--;) {
                a = i[u];
                if (a.operator ? !a.test(this.getAttribute(e, a.key)) : !this.hasAttribute(e, a.key)) return ! 1
            }
            if (s) for (u = s.length; u--;) {
                a = s[u];
                if (!this.matchPseudo(e, a.key, a.value)) return ! 1
            }
            return ! 0
        };
        var o = {
            " ": function(e, t, n, r, i, s, o) {
                var u, a, f;
                if (this.isHTMLDocument) {
                    e: if (n) {
                        a = this.document.getElementById(n);
                        if (!a && e.all || this.idGetsName && a && a.getAttributeNode("id").nodeValue != n) {
                            f = e.all[n];
                            if (!f) return;
                            f[0] || (f = [f]);
                            for (u = 0; a = f[u++];) {
                                var l = a.getAttributeNode("id");
                                if (l && l.nodeValue == n) {
                                    this.push(a, t, null, r, i, s);
                                    break
                                }
                            }
                            return
                        }
                        if (!a) {
                            if (this.contains(this.root, e)) return;
                            break e
                        }
                        if (this.document !== e && !this.contains(e, a)) return;
                        this.push(a, t, null, r, i, s);
                        return
                    }
                    t: if (r && e.getElementsByClassName && !this.brokenGEBCN) {
                        f = e.getElementsByClassName(o.join(" "));
                        if (!f || !f.length) break t;
                        for (u = 0; a = f[u++];) this.push(a, t, n, null, i, s);
                        return
                    }
                }
                n: {
                    f = e.getElementsByTagName(t);
                    if (!f || !f.length) break n;
                    this.brokenStarGEBTN || (t = null);
                    for (u = 0; a = f[u++];) this.push(a, t, n, r, i, s)
                }
            },
            ">": function(e, t, n, r, i, s) {
                if (e = e.firstChild) do e.nodeType == 1 && this.push(e, t, n, r, i, s);
                while (e = e.nextSibling)
            },
            "+": function(e, t, n, r, i, s) {
                while (e = e.nextSibling) if (e.nodeType == 1) {
                    this.push(e, t, n, r, i, s);
                    break
                }
            },
            "^": function(e, t, n, r, i, s) {
                e = e.firstChild,
                e && (e.nodeType == 1 ? this.push(e, t, n, r, i, s) : this["combinator:+"](e, t, n, r, i, s))
            },
            "~": function(e, t, n, r, i, s) {
                while (e = e.nextSibling) {
                    if (e.nodeType != 1) continue;
                    var o = this.getUID(e);
                    if (this.bitUniques[o]) break;
                    this.bitUniques[o] = !0,
                    this.push(e, t, n, r, i, s)
                }
            },
            "++": function(e, t, n, r, i, s) {
                this["combinator:+"](e, t, n, r, i, s),
                this["combinator:!+"](e, t, n, r, i, s)
            },
            "~~": function(e, t, n, r, i, s) {
                this["combinator:~"](e, t, n, r, i, s),
                this["combinator:!~"](e, t, n, r, i, s)
            },
            "!": function(e, t, n, r, i, s) {
                while (e = e.parentNode) e !== this.document && this.push(e, t, n, r, i, s)
            },
            "!>": function(e, t, n, r, i, s) {
                e = e.parentNode,
                e !== this.document && this.push(e, t, n, r, i, s)
            },
            "!+": function(e, t, n, r, i, s) {
                while (e = e.previousSibling) if (e.nodeType == 1) {
                    this.push(e, t, n, r, i, s);
                    break
                }
            },
            "!^": function(e, t, n, r, i, s) {
                e = e.lastChild,
                e && (e.nodeType == 1 ? this.push(e, t, n, r, i, s) : this["combinator:!+"](e, t, n, r, i, s))
            },
            "!~": function(e, t, n, r, i, s) {
                while (e = e.previousSibling) {
                    if (e.nodeType != 1) continue;
                    var o = this.getUID(e);
                    if (this.bitUniques[o]) break;
                    this.bitUniques[o] = !0,
                    this.push(e, t, n, r, i, s)
                }
            }
        };
        for (var u in o) e["combinator:" + u] = o[u];
        var a = {
            empty: function(e) {
                var t = e.firstChild;
                return (!t || t.nodeType != 1) && !(e.innerText || e.textContent || "").length
            },
            not: function(e, t) {
                return ! this.matchNode(e, t)
            },
            contains: function(e, t) {
                return (e.innerText || e.textContent || "").indexOf(t) > -1
            },
            "first-child": function(e) {
                while (e = e.previousSibling) if (e.nodeType == 1) return ! 1;
                return ! 0
            },
            "last-child": function(e) {
                while (e = e.nextSibling) if (e.nodeType == 1) return ! 1;
                return ! 0
            },
            "only-child": function(e) {
                var t = e;
                while (t = t.previousSibling) if (t.nodeType == 1) return ! 1;
                var n = e;
                while (n = n.nextSibling) if (n.nodeType == 1) return ! 1;
                return ! 0
            },
            "nth-child": e.createNTHPseudo("firstChild", "nextSibling", "posNTH"),
            "nth-last-child": e.createNTHPseudo("lastChild", "previousSibling", "posNTHLast"),
            "nth-of-type": e.createNTHPseudo("firstChild", "nextSibling", "posNTHType", !0),
            "nth-last-of-type": e.createNTHPseudo("lastChild", "previousSibling", "posNTHTypeLast", !0),
            index: function(e, t) {
                return this["pseudo:nth-child"](e, "" + t + 1)
            },
            even: function(e) {
                return this["pseudo:nth-child"](e, "2n")
            },
            odd: function(e) {
                return this["pseudo:nth-child"](e, "2n+1")
            },
            "first-of-type": function(e) {
                var t = e.nodeName;
                while (e = e.previousSibling) if (e.nodeName == t) return ! 1;
                return ! 0
            },
            "last-of-type": function(e) {
                var t = e.nodeName;
                while (e = e.nextSibling) if (e.nodeName == t) return ! 1;
                return ! 0
            },
            "only-of-type": function(e) {
                var t = e,
                n = e.nodeName;
                while (t = t.previousSibling) if (t.nodeName == n) return ! 1;
                var r = e;
                while (r = r.nextSibling) if (r.nodeName == n) return ! 1;
                return ! 0
            },
            enabled: function(e) {
                return ! e.disabled
            },
            disabled: function(e) {
                return e.disabled
            },
            checked: function(e) {
                return e.checked || e.selected
            },
            focus: function(e) {
                return this.isHTMLDocument && this.document.activeElement === e && (e.href || e.type || this.hasAttribute(e, "tabindex"))
            },
            root: function(e) {
                return e === this.root
            },
            selected: function(e) {
                return e.selected
            }
        };
        for (var f in a) e["pseudo:" + f] = a[f];
        var l = e.attributeGetters = {
            "class": function() {
                return this.getAttribute("class") || this.className
            },
            "for": function() {
                return "htmlFor" in this ? this.htmlFor: this.getAttribute("for")
            },
            href: function() {
                return "href" in this ? this.getAttribute("href", 2) : this.getAttribute("href")
            },
            style: function() {
                return this.style ? this.style.cssText: this.getAttribute("style")
            },
            tabindex: function() {
                var e = this.getAttributeNode("tabindex");
                return e && e.specified ? e.nodeValue: null
            },
            type: function() {
                return this.getAttribute("type")
            },
            maxlength: function() {
                var e = this.getAttributeNode("maxLength");
                return e && e.specified ? e.nodeValue: null
            }
        };
        l.MAXLENGTH = l.maxLength = l.maxlength;
        var c = e.Slick = this.Slick || {};
        c.version = "1.1.6",
        c.search = function(t, n, r) {
            return e.search(t, n, r)
        },
        c.find = function(t, n) {
            return e.search(t, n, null, !0)
        },
        c.contains = function(t, n) {
            return e.setDocument(t),
            e.contains(t, n)
        },
        c.getAttribute = function(t, n) {
            return e.setDocument(t),
            e.getAttribute(t, n)
        },
        c.hasAttribute = function(t, n) {
            return e.setDocument(t),
            e.hasAttribute(t, n)
        },
        c.match = function(t, n) {
            return ! t || !n ? !1 : !n || n === t ? !0 : (e.setDocument(t), e.matchNode(t, n))
        },
        c.defineAttributeGetter = function(t, n) {
            return e.attributeGetters[t] = n,
            this
        },
        c.lookupAttributeGetter = function(t) {
            return e.attributeGetters[t]
        },
        c.definePseudo = function(t, n) {
            return e["pseudo:" + t] = function(e, t) {
                return n.call(e, t)
            },
            this
        },
        c.lookupPseudo = function(t) {
            var n = e["pseudo:" + t];
            return n ?
            function(e) {
                return n.call(this, e)
            }: null
        },
        c.override = function(t, n) {
            return e.override(t, n),
            this
        },
        c.isXML = e.isXML,
        c.uidOf = function(t) {
            return e.getUIDHTML(t)
        },
        this.Slick || (this.Slick = c)
    }.apply(typeof exports != "undefined" ? exports: this),
    e.__getElements = function(e, t) {
        return Slick.search(e, t)
    },
    e.__getElement = function(e, t) {
        return Slick.find(e, t)
    }
})(this),
String.prototype.trim = function() {
    return String(this).replace(/^\s+|\s+$/g, "")
},
Array.indexOf || (Array.prototype.indexOf = function(e) {
    for (var t = 0; t < this.length; t++) if (this[t] == e) return t;
    return - 1
}),
function() {
    function getHref(e) {
        return e = e || "",
        e.indexOf("//") == 0 ? e = location.protocol + e: e.indexOf("http") < 0 && (e = location.protocol + "//" + location.hostname + e),
        e
    }
    function getAttribute(e, t) {
        return e && e.getAttribute && e.getAttribute(t) || ""
    }
    function getClass(e) {
        return getAttribute(e, "class")
    }
    function hasClass(e, t) {
        return getClass(e).indexOf(t) >= 0
    }
    function tagName(e) {
        return (e && e.tagName || "").toLowerCase()
    }
    function registerImagesForPinBtn(e) {
        for (var t = 0; t < e.length; t++) registerImageForPinBtn(e[t])
    }
    function registerImageForPinBtn(e) {
        var t = e.container || e.img;
        if (t && !t.getAttribute("data-pinit")) {
            t.setAttribute("data-pinit", "registered");
            var n = [t.onmouseover ||
            function() {},
            t.onmouseout ||
            function() {},
            t.onmousemove ||
            function() {}];
            t.onmouseover = function(r) {
                return r = r || window.event,
                getToggleOn(function(t) {
                    t && !isShowedBtn && (isShowedBtn = !0, showPinBtn(e))
                }),
                n[0].call(t, r)
            },
            t.onmouseout = function(e) {
                return e = e || window.event,
                hidePinBtn(),
                isShowedBtn = !1,
                n[1].call(t, e)
            },
            t.onmousemove = function(r) {
                return r = r || window.event,
                getToggleOn(function(t) {
                    t && !isShowedBtn && (isShowedBtn = !0, showPinBtn(e))
                }),
                n[2].call(t, r)
            }
        }
    }
    function generatePinBtn() {
        if (!document.getElementById(global + "_Button")) {
            pinBtn = generateTag("Button", "pinit"),
            pinBtn.onmouseover = function() {
                selectedText = getSelectedText(),
                showPinBtn()
            },
            pinBtn.onmouseout = function() {
                hidePinBtn()
            };
            if (isShareBtn) pinBtn.onclick = function() {
                return currentImage && pinImage(currentImage),
                selectedText = "",
                itemUrl = "",
                !1
            };
            else {
                var e = generateTag("thunderpinBtn", "a");
                e.href = "#",
                e.title = "蹇€熼噰闆�",
                e.onclick = "return false;",
                e.innerHTML = "<strong><em></em></strong>";
                var t = generateTag("pinBtn", "a");
                t.href = "#",
                t.title = "閲囬泦鍒拌姳鐡�",
                t.onclick = "return false;",
                t.innerHTML = "閲囬泦鍒拌姳鐡�",
                isIE() ? (e.className = "thunderpin", t.className = "pin") : (e.setAttribute("class", "thunderpin"), t.setAttribute("class", "pin")),
                pinBtn.appendChild(e),
                pinBtn.appendChild(t),
                pinBtn.style.display = "none",
                t.onclick = function() {
                    return currentImage && pinImage(currentImage),
                    selectedText = "",
                    itemUrl = "",
                    !1
                },
                e.onclick = function() {
                    var e = {
                        top: pinBtn.style.top,
                        left: pinBtn.style.left
                    };
                    return currentImage && thunderpinImage(currentImage, null, e) && (selectedText = "", itemUrl = ""),
                    !1
                }
            }
            document.body.appendChild(pinBtn)
        } else pinBtn = document.getElementById(global + "_Button");
        var n = global + "_Button_";
        if (isShareBtn && pinBtn) {
            n = global + "_Button_share_";
            var r = n + (~btnPositions.indexOf("rigth") ? " right": "left"),
            i = n + (~btnPositions.indexOf("bottom") ? "bottom": "top");
            isIE() ? pinBtn.className = global + "_Button_share " + r + " " + i: pinBtn.setAttribute("class", global + "_Button_share " + r + " " + i)
        }
    }
    function showPinBtn(e) {
        clearTimeout(hidePinBtnTimer);
        var t = ~btnPositions.indexOf("right") ? "right": "left",
        n = ~btnPositions.indexOf("bottom") ? "bottom": "top";
        if (e) {
            var r = e.container || e.img,
            i, s;
            s = i = 0,
            currentImage = e;
            if (r.getBoundingClientRect) {
                var o = document.documentElement,
                u = r.getBoundingClientRect(),
                a = o.clientTop || document.body.clientTop || 0,
                f = window.pageYOffset || document.body.scrollTop,
                l = 0,
                c = 0;
                currentImage._parentNode && (l = currentImage._parentNode.offsetTop || 0, c = currentImage._parentNode.offsetLeft || 0),
                i = u.left + (window.pageXOffset || document.body.scrollLeft) - (o.clientLeft || document.body.clientLeft || 0) + c,
                s = u.top + f - a + l,
                t == "right" && (i += u.width ? u.width - 86 : r.width - 86),
                n == "bottom" && (s += u.height ? u.height - 24 : r.height - 24)
            }
            isIE() && document.documentElement && !Browser.ie9 && (document.documentElement.scrollTop && (s += document.documentElement.scrollTop), document.documentElement.scrollLeft && (i += document.documentElement.scrollLeft)),
            n == "bottom" ? s += 24 : s -= isShareBtn ? 24 : 26,
            t == "right" ? i += isShareBtn ? 6 : -16 : i -= isShareBtn ? 0 : 2,
            pinBtn.style.top = (s > 0 ? s: 0) + "px",
            pinBtn.style.left = (i > 0 ? i: 0) + "px";
            if (important) {
                var h = " top:" + (s > 0 ? s: 0) + "px !important;" + " left:" + (i > 0 ? i: 0) + "px !important;";
                pinBtn.setAttribute("style", h)
            }
        }
        isIE() ? (pinBtn.style.display = "block", pinBtn.style.visibility = "visible") : (pinBtn.style.display = "block", pinBtn.style.display = "block !important", pinBtn.style.visibility = "visible", pinBtn.style.visibility = "visible !important");
        if (important) {
            var h = pinBtn.getAttribute("style") + (isIE() ? ";": "") + " display: block !important; visibility: visible !important;";
            pinBtn.setAttribute("style", h)
        }
    }
    function hidePinBtn() {
        hidePinBtnTimer = setTimeout(function() {
            isIE() ? (pinBtn.style.display = "none", pinBtn.style.visibility = "hidden") : (pinBtn.style.display = "none", pinBtn.style.display = "none !important", pinBtn.style.visibility = "hidden", pinBtn.style.visibility = "hidden !important");
            if (important) {
                var e = " display: none !important; visibility: hidden !important;";
                pinBtn.setAttribute("style", e)
            }
            currentImage = null
        },
        100)
    }
    function calculateMarginTop(e) {
        return Math.max(e.h, e.w) > 199 ? e.h < e.w ? parseInt(100 - 100 * (e.h / e.w)) + "px": "": parseInt(100 - e.h / 2) + "px"
    }
    function generateStyleElement() {
        var e = global + "_Style";
        if (document.getElementById(e)) return;
        var t = "#PREFIX_Container {font-family: 'helvetica neue', arial, sans-serif; position: absolute; padding-top: 37px; z-index: 100000002; top: 0; left: 0; background-color: transparent; opacity: 1;hasLayout:-1;}#PREFIX_Overlay {position: fixed; z-index: 100000001; top: 0; right: 0; bottom: 0; left: 0; background-color: #f2f2f2; opacity: .95;}* html #PREFIX_Overlay {position: absolute;}#PREFIX_Control {position:relative; z-index: 100000; float: left; background-color: #fcf9f9; border: solid #ccc; border-width: 0 1px 1px 0; height: 200px; width: 200px; opacity: 1;}* html #PREFIX_Control {position:static;}#PREFIX_Control img {position: relative; padding: 0; display: block; margin: 82px auto 0; -ms-interpolation-mode: bicubic;}#PREFIX_Control a {position: fixed; z-index: 10001; right: 0; top: 0; left: 0; height: 24px; padding: 12px 0 0; text-align: center; font-size: 14px; line-height: 1em; text-shadow: 0 1px #fff; color: #211922; font-weight: bold; text-decoration: none; background: #fff url(ASSETS_URL/fullGradient07Normal.png) 0 0 repeat-x; border-bottom: 1px solid #ccc; -mox-box-shadow: 0 0 2px #d7d7d7; -webkit-box-shadow: 0 0 2px #d7d7d7;}* html #PREFIX_Control a {position: absolute; width: 100%;}#PREFIX_Control a:hover {color: #fff; text-decoration: none; background-color: #1389e5; border-color: #1389e5; text-shadow: 0 -1px #46A0E6;}#PREFIX_Control a:active {height: 23px; padding-top: 13px; background-color: #211922; border-color: #211922; background-image: url(ASSETS_URL/fullGradient07Inverted.png); text-shadow: 0 -1px #211922;}.PREFIXImagePreview {position: relative; padding: 0; margin: 0; float: left; background-color: #fff; border: solid #e7e7e7; border-width: 0 1px 1px 0; height: 200px; width: 200px; opacity: 1; z-index: 10002; text-align: center; overflow:hidden;}.PREFIXImagePreview .PREFIXVideoIcon {position:absolute;display:block;top:0;left:0;width:100%;height:100%;background:url(ASSETS_URL/media_video.png) center center no-repeat;}.PREFIXImagePreview .PREFIXImg {border: none; height: 200px; width: 200px; opacity: 1; padding: 0; position: absolute; top: 0; left: 0;}.PREFIXImagePreview .PREFIXImg a {margin: 0; padding: 0; position: absolute; top: 0; bottom: 0; right: 0; left: 0; display: block; text-align: center;  z-index: 1;}.PREFIXImagePreview .PREFIXImg a:hover {background-color: #fcf9f9; border: none;}.PREFIXImagePreview .PREFIXImg .ImageToPin {max-height: 200px; max-width: 200px; width: auto !important; height: auto !important;}.PREFIXImagePreview img.PREFIX_PinIt {border: none; position: absolute; top: 82px; left: 42px; display: none; padding: 0; background-color: transparent; z-index: 100;}.PREFIXImagePreview strong {text-indent: -9999px; position: absolute; top: 82px; display: none; height: 32px; background: url(ASSETS_URL/bm_pin_sprite.png?20120918) no-repeat 0 0;}.PREFIXImagePreview strong.PREFIX_ThunderPin {width: 24px; left: 52px; background-position: 0 0;}.PREFIXImagePreview strong.PREFIX_ThunderPin:hover {background-position: 0 -50px;}.PREFIXImagePreview strong.PREFIX_ThunderPin:active {background-position: 0 -100px;}.PREFIXImagePreview strong.PREFIX_Pin {width: 72px; left: 75px; background-position: -40px 0;}.PREFIXImagePreview strong.PREFIX_Pin:hover {background-position: -40px -50px;}.PREFIXImagePreview strong.PREFIX_Pin:active {background-position: -40px -100px;}.PREFIXImagePreview img.PREFIX_vidind {border: none; position: absolute; top: 75px; left: 75px; padding: 0; background-color: transparent; z-index: 99;}.PREFIXDimensions { color: #000; position: relative; margin-top: 180px; text-align: center; font-size: 10px; z-index:10003; display: inline-block; background: white; border-radius: 4px; padding: 0 2px;}#PREFIX_Button, #PREFIX_Button *, #PREFIX_Container, #PREFIX_Container * { -webkit-box-sizing: content-box; -moz-box-sizing: content-box; -ms-box-sizing: content-box; box-sizing: content-box;}#PREFIX_Button { display: none; position: absolute; z-index: 999999999 !important; color: #211922; text-shadow: 0 1px #eaeaea; font: 12px/1 'Helvetica Neue',Helvetica,Arial,Sans-serif; text-align: center; padding: 0; margin: 0; cursor: pointer;}#PREFIX_Button a {text-decoration: none; color: #211922; display: inline-block; text-align: center; line-height: 14px; height: 14px; border-radius: 2px; -webkit-border-radius: 2px; -moz-border-radius: 2px; -ms-border-radius: 2px; -o-border-radius: 2px; cursor: pointer; position: absolute; top: 0; left: 0; height: 14px; margin: 0 2px; padding: 5px 8px; border: 1px solid #555; border: 1px solid rgba(140, 126, 126, .5); background-color: #fff;}#PREFIX_Button a:hover {text-decoration: none; background-image: -webkit-linear-gradient(top, #fefeff, #efefef); background-image: -moz-linear-gradient(top, #fefeff, #efefef); box-shadow: inset 0 1px rgba(255,255,255,0.35), 0 1px 1px rgba(35,24,24,0.75); -o-box-shadow: inset 0 1px rgba(255,255,255,0.35), 0 1px 1px rgba(35,24,24,0.75); -ms-box-shadow: inset 0 1px rgba(255,255,255,0.35), 0 1px 1px rgba(35,24,24,0.75); -moz-box-shadow: inset 0 1px rgba(255,255,255,0.35), 0 1px 1px rgba(35,24,24,0.75); -webkit-box-shadow: inset 0 1px rgba(255,255,255,0.35), 0 1px 1px rgba(35,24,24,0.75);}#PREFIX_Button a:active {text-decoration: none; background-image: -webkit-linear-gradient(top, #fefeff, #efefef); background-image: -moz-linear-gradient(top, #fefeff, #efefef); box-shadow: inset 0 1px 2px rgba(34,25,25,0.25), 0 0 1px rgba(232,230,230,0.5); -o-box-shadow: inset 0 1px 2px rgba(34,25,25,0.25), 0 0 1px rgba(232,230,230,0.5); -ms-box-shadow: inset 0 1px 2px rgba(34,25,25,0.25), 0 0 1px rgba(232,230,230,0.5); -moz-box-shadow: inset 0 1px 2px rgba(34,25,25,0.25), 0 0 1px rgba(232,230,230,0.5); -webkit-box-shadow: inset 0 1px 2px rgba(34,25,25,0.25), 0 0 1px rgba(232,230,230,0.5);}#PREFIX_Button a strong {position: relative; line-height: 12px;}#PREFIX_Button a.thunderpin {margin-right: 0; border-right: none; width: 14px; padding: 5px 0 5px 4px; border-top-right-radius: 0; border-bottom-right-radius: 0; -webkit-border-top-right-radius: 0; -webkit-border-bottom-right-radius: 0; -moz-border-top-right-radius: 0; -moz-border-bottom-right-radius: 0; -ms-border-top-right-radius: 0; -ms-border-bottom-right-radius: 0; -o-border-top-right-radius: 0; -o-border-bottom-right-radius: 0;}#PREFIX_Button a.thunderpin em {background: url(ASSETS_URL/ActionIcons10.png?20120801) no-repeat -30px 0; position: relative; display: inline-block; width: 10px; height: 10px; top: 1px; left: -2px;}#PREFIX_Button a.thunderpin:hover em {background-image-postion: -30px -10px;}#PREFIX_Button a.thunderpin:active em {background-image-postion: -30px -20px;}#PREFIX_Button a.pin {left: 20px; width: 64px; margin-left: 0; *margin-left: -2px; border-top-left-radius: 0; border-bottom-left-radius: 0; -webkit-border-top-left-radius: 0; -webkit-border-bottom-left-radius: 0; -moz-border-top-left-radius: 0; -moz-border-bottom-left-radius: 0; -ms-border-top-left-radius: 0; -ms-border-bottom-left-radius: 0; -o-border-top-left-radius: 0; -o-border-bottom-left-radius: 0;}.PREFIX_Button_share {text-indent: -9999px; width: 68px; height: 24px; padding:0; background: url(ASSETS_URL/sharebutton_sprite.png?20121226) no-repeat 0 -80px !important; border: none;}.PREFIX_Button_share:hover {background-position: 0 -120px; background-position: 0 -120px !important;}.PREFIX_Button_share_top {background-position: 0 -80px; background-position: 0 -80px !important;}.PREFIX_Button_share_top:hover {background-position: 0 -120px; background-position: 0 -120px !important;}.PREFIX_Button_share_bottom {background-position: 0 0; background-position: 0 0 !important;}.PREFIX_Button_share_bottom:hover {background-position: 0 -40px; background-position: 0 -40px !important;}.PREFIX_thunder_tip {position: absolute; z-index: 999999999 !important; background: #000; background: rgba(0,0,0,0.5); color: white; line-height: 16px; padding: 5px; border-radius: 2px; margin-left: 2px; }.PREFIX_thunder_tip a {text-shadow: none; cursor: pointer; padding: 0 4px; margin: 0 2px; color: white; font-size: 13px; background: rgba(255, 255, 255, 0.4); }.PREFIX_thunder_tip a:hover {color: #B90000; background: white; text-decoration: none; }.PREFIXImagePreview .PREFIX_thunder_tip {line-height: 12px; padding: 8px 10px; font-size: 14px; top: 50%; left: 50%; margin-left: -48px; margin-top: -18px;}.PREFIXImagePreview .PREFIX_thunder_tip_warning {left: 48px; height: auto; text-align: left;}.PREFIX_thunder_tip_success {color: #fff;font-weight: bold;}.PREFIX_thunder_tip p {font-weight: normal; margin-top: 2px; margin-bottom: 0; padding-left: 20px; text-align: left;}.PREFIX_thunder_tip a {color: #fff;}.PREFIX_thunder_tip_failed {height: 32px; font-weight: bold; color: #fff;background: #c90000; background: rgba(201, 0, 0, .5); }.PREFIX_thunder_tip_failed p {margin: 0 2px; font-weight: normal; font-size: 12px;}.PREFIX_thunder_tip span { padding-left: 22px; position: relative;}.PREFIX_thunder_tip_warning span {display: block; line-height: 18px;}.PREFIX_thunder_tip span em { background: url(ASSETS_URL/bm_pin_sprite.png?20120918) no-repeat 0px -150px; display: inline-block; height: 16px; width: 16px; position: absolute; left: 0; top: 50%; margin-top: -8px;}.PREFIX_thunder_tip_success span em { background: url(ASSETS_URL/bm_pin_sprite.png?20120918) no-repeat 0px -150px;}.PREFIX_thunder_tip_warning span em { top: 9px; left: 0px; background: url(ASSETS_URL/bm_pin_sprite.png?20120918) no-repeat -80px -150px;}.PREFIX_thunder_tip_failed span em { background: url(ASSETS_URL/bm_pin_sprite.png?20120918) no-repeat -40px -150px;}.PREFIX_thunder_tip_ing span em { background: url(ASSETS_URL/thunder_motion.gif) no-repeat 2px 2px;}.PREFIXImagePreview .PREFIX_thunder_tip_failed {width: 140px; margin-left: -80px; margin-top: -26px;}.PREFIXImagePreview .PREFIX_thunder_tip_success {width: 88px; margin-left: -52px; margin-top: -26px;}.PREFIXImagePreview .PREFIX_thunder_tip_ing {width: 72px;}.PREFIXImagePreview .PREFIX_thunder_tip_success p, .PREFIXImagePreview .PREFIX_thunder_tip_failed p {margin-top: 9px; font-size: 12px; display: block;}".replace(/PREFIX/g, global).replace(/ASSETS_URL/g, imageRoot),
        n = document.createElement("style");
        n.id = e,
        isIE() && (n.type = "text/css", n.media = "screen"),
        (document.getElementsByTagName("head")[0] || document.body).appendChild(n),
        n.styleSheet ? n.styleSheet.cssText = t: n.appendChild(document.createTextNode(t))
    }
    function generateTag(e, t) {
        var n = document.createElement(t || "div");
        return n.id = global + "_" + e,
        n
    }
    function encapsulateImage(e) {
        var t = new Image;
        t.src = e.src;
        var n = {
            w: e.naturalWidth || e.width,
            h: e.naturalHeight || e.height,
            src: e.src,
            img: e,
            alt: "",
            img2: t
        };
        return n
    }
    function isValidImage(e) {
        return e.src && e.src.indexOf("data:") == 0 ? !1 : e.style.display != "none" && e.className != "ImageToPin" && e.width >= minWidth && e.height >= minHeight ? !0 : !1
    }
    
    function getVideoOnCustomerPage(e, t) {
        var n = function(e, n) {
            var r = new Image;
            if (e.indexOf("player.youku.com/player") > 0 || e.indexOf("www.tudou.com") > 0 || e.indexOf("player.ku6.com/refer") > 0 || e.indexOf("player.56.com") > 0) r.src = "http://" + siteDomain + "/pins/create/video/swf?url=" + encodeURIComponent(e),
            r.width = 448,
            r.height = 336,
            r = encapsulateImage(r),
            r.container = n,
            r.video = e,
            r.media_type = 1,
            t.push(r);
            else if (e.indexOf("share.vrs.sohu.com") > 0) if (e.indexOf("share.vrs.sohu.com/my") > 0) {
                var i = /share.vrs.sohu.com\/my\/v.swf.+?&id=(.+?)&autoplay=false/,
                s = i.exec(e);
                if (!s) return ! 1;
                s = s[1],
                r.src = "http://" + siteDomain + "/pins/create/video/mysohu/?id=" + s,
                r.width = 480,
                r.height = 360,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            } else {
                var i = /share\.vrs\.sohu\.com\/(.+?)\/v\.swf/,
                s = i.exec(e);
                if (!s) return ! 1;
                s = s[1],
                r.src = "http://" + siteDomain + "/pins/create/video/sohu/?id=" + s,
                r.width = 480,
                r.height = 360,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            } else if (e.indexOf("v.ifeng.com/include/exterior.swf") > 0) {
                var i = /guid=(.+?)&/,
                s = i.exec(e);
                if (!s) return ! 1;
                s = s[1],
                r.src = "http://" + siteDomain + "/pins/create/video/ifeng/?id=" + s,
                r.width = 480,
                r.height = 360,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            } else if (e.indexOf("manhua1.appsina.com") > 0 || e.indexOf("weibo.vmanhua.com") > 0) r.src = "http://" + siteDomain + "/pins/create/video/swf?url=" + e,
            r.width = 187,
            r.height = 255,
            r = encapsulateImage(r),
            r.container = n,
            r.video = e,
            r.media_type = 1,
            t.push(r);
            else if (e.indexOf("swf.ws.126.net/movieplayer") > 0) {
                var i = /-(vimg.+)-.swf?/,
                s = i.exec(e);
                if (!s) return ! 1;
                s = s[1],
                s = s.replace(/_/g, "."),
                r.src = "http://" + s + ".jpg",
                r.width = 480,
                r.height = 360,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            } else if (e.indexOf("swf.ws.126.net/v") > 0) {
                var i = /coverpic=\"(.+?)&/,
                s = i.exec(e);
                if (!s) return ! 1;
                s = s[1],
                r.src = s,
                r.width = 480,
                r.height = 360,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            } else if (e.indexOf("player.yinyuetai.com") > 0) {
                var i = /player\/(.+?)\//,
                s = i.exec(e);
                if (!s) return ! 1;
                s = s[1],
                e.indexOf("video") > 0 ? r.src = "http://" + siteDomain + "/pins/create/video/yinyuetai/?id=" + s: r.src = "http://" + siteDomain + "/pins/create/video/yytList/?id=" + s,
                r.width = 480,
                r.height = 360,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            } else if (e.indexOf("player.video.qiyi.com") > 0) {
                var i = /com\/(.+?)\//,
                s = i.exec(e);
                if (!s) return ! 1;
                s = s[1],
                r.src = "http://" + siteDomain + "/pins/create/video/qiyi/?id=" + s,
                r.width = 115,
                r.height = 77,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            } else if (e.indexOf("www.jifenzhong.com/external") > 0) {
                var i = /v1.0\/(.+?)\/player/,
                s = i.exec(e);
                if (!s) return ! 1;
                s = s[1],
                r.src = "http://" + siteDomain + "/pins/create/video/jfz/?id=" + s,
                r.width = 480,
                r.height = 305,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            } else if (e.indexOf("player.pptv.com/v") > 0) r.src = "http://" + siteDomain + "/pins/create/video/swf?url=" + e,
            r.width = 120,
            r.height = 60,
            r = encapsulateImage(r),
            r.container = n,
            r.video = e,
            r.media_type = 1,
            t.push(r);
            else if (e.indexOf("static.video.qq.com") > 0) {
                var i = /vid=(.+)&/,
                s = i.exec(e);
                r.src = "http://vpic.video.qq.com/76082551/" + s[1] + "_160_90_3.jpg",
                r.width = 160,
                r.height = 90,
                r = encapsulateImage(r),
                r.container = n,
                r.video = e,
                r.media_type = 1,
                t.push(r)
            }
        };
        for (u = 0; u < e.embeds.length; u++) {
            var r = e.embeds[u];
            if (tagName(r.parentNode) == "object" && r.src.indexOf("player.youku.com") <= 0) continue;
            var i = r.src,
            s = r.getAttribute("flashvars");
            if (s && i.indexOf("www.56.com") > 0) {
                s = s.split("&");
                var o;
                for (var u = 0; u < s.length; u++) {
                    o = s[u].split("=");
                    if (o[0] == "vid") {
                        i = "http://player.56.com/v_" + o[1] + ".swf";
                        break
                    }
                }
            }
            n(i, r)
        }
        var a = document.getElementsByTagName("object");
        for (u = 0; u < a.length; u++) {
            if (tagName(a[u].parentNode) == "object") continue;
            var i = __getElement(a[u], "param[name=movie], param[name=src]");
            if (i) {
                var f = a[u];
                i = getAttribute(i, "value");
                var s = __getElement(a[u], "param[name=FlashVars]");
                if (s && i.indexOf("www.56.com") > 0) {
                    s = getAttribute(s, "value").split("&");
                    var o;
                    for (var u = 0; u < s.length; u++) {
                        o = s[u].split("=");
                        if (o[0] == "vid") {
                            i = "http://player.56.com/v_" + o[1] + ".swf";
                            break
                        }
                    }
                }
                if (i.indexOf("swf.ws.126.net/v") > 0) {
                    var l = /value=\"pltype(.+?)\"\s+name=\"flashvars\"/,
                    c = l.exec(a[u].innerHTML);
                    c && c[1] && (param = c[1], param = param.replace(/&amp;/g, "&"), i = i + "?pltype" + param)
                }
                n(i, f.parentNode || f)
            }
        }
    }
    function getCurrentPageImagesWithEncapsulation(d, eImages, opts) {
        var _document = d || document;
        eImages = eImages || [],
        opts = opts || {};
        if (skip) return eImages;
        for (i = 0; i < _document.images.length; i++) {
            var img = _document.images[i];
            isValidImage(img) && (img = encapsulateImage(img), opts && (img._parentNode = opts.parentNode || null), eImages.push(img))
        }
        getVideoOnCustomerPage(_document, eImages);
        var bgimgs_reg;
        for (i in bgimgs) {
            bgimgs_reg = new RegExp(i);
            if (bgimgs_reg.test(location.href)) {
                var imgs = bgimgs[i]();
                if (!imgs) break;
                for (var i = 0; i < imgs.length; i++) opts && (imgs[i].img._parentNode = opts.parentNode || null),
                eImages.push(imgs[i]);
                break
            }
        }
        var url = _document.location.href,
        thumb = new Image,
        scripts = _document.getElementsByTagName("script");
        if (url.indexOf("www.tudou.com") > 0 && _document.getElementById("playerObject")) {
            thumb.src = itemData.pic,
            thumb.width = 320,
            thumb.height = 240,
            thumb = encapsulateImage(thumb),
            thumb.container = _document.getElementById("playerObject");
            var video = ""; ! video && !_document.getElementById("copyInput") && (_document.getElementById("shareMore").click(), _document.getElementsByClassName("btn_share_flash")[0].click(), video = _document.getElementById("copyInput").value),
            thumb.video = video,
            thumb.media_type = 1,
            eImages.push(thumb)
        } else if (url.indexOf("www.bilibili.tv") > 0) {
            var datas = document.getElementsByTagName("meta"),
            pic = "",
            video = "";
            for (var i = 0; i < datas.length; i++) {
                if (datas[i].getAttribute("itemprop") == "thumbnailUrl") {
                    pic = datas[i].getAttribute("content");
                    continue
                }
                if (datas[i].getAttribute("itemprop") == "embedURL") {
                    video = datas[i].getAttribute("content");
                    continue
                }
            }
            pic && video && (thumb.src = pic, thumb.width = 120, thumb.height = 90, thumb = encapsulateImage(thumb), thumb.container = _document.getElementById("bofqi"), thumb.video = video, thumb.media_type = 1, eImages.push(thumb))
        } else if (url.indexOf("www.acfun.tv") > 0) {
            var pic = system.preview,
            video = "http://w5cdn.ranktv.cn/player/ACFlashPlayerX.3rd.20130407.swf?type=page&url=" + url;
            pic && video && (thumb.src = pic, thumb.width = 120, thumb.height = 90, thumb = encapsulateImage(thumb), thumb.container = _document.getElementById("area-player"), thumb.video = video, thumb.media_type = 1, eImages.push(thumb))
        } else if (url.indexOf("v.163.com/special") > 0 || url.indexOf("v.163.com/movie") > 0) {
            var video, vWidth, vHeight, reg, m, coverImg;
            for (var i = 0; i < scripts.length; i++) if (!scripts[i].src && scripts[i].textContent.indexOf("flashPlayer") != -1) {
                reg = /new flashPlayer\(\"(.+?)\",(\d+),(\d+)\);?/,
                m = reg.exec(scripts[i].textContent);
                if (m && m[1]) {
                    video = m[1],
                    vWidth = m[2],
                    vHeight = m[3];
                    break
                }
            }
            video && vWidth && vHeight && (reg = /-(vimg.+)-.swf?/, m = reg.exec(video), coverImg = m[1].replace(/_/g, "."), coverImg = "http://" + coverImg + ".jpg", thumb.src = coverImg, thumb.width = vWidth, thumb.height = vHeight, thumb = encapsulateImage(thumb), thumb.container = _document.getElementById("flashArea"), thumb.video = video, thumb.media_type = 1, eImages.push(thumb))
        } else if (url.indexOf("v.163.com/zixun") > 0 || url.indexOf("v.163.com/zongyi") > 0 || url.indexOf("v.163.com/jishi") > 0) {
            var video, reg, m, coverImg;
            for (var i = 0; i < scripts.length; i++) if (!scripts[i].src && scripts[i].textContent.indexOf("flashPlayer") != -1) {
                reg = /data=\"(.+?)\"/,
                m = reg.exec(scripts[i].textContent);
                if (m && m[1]) {
                    video = m[1],
                    reg = /value=\"pltype(.+?)\"\s+name=\"flashvars\"/,
                    m = reg.exec(scripts[i].textContent),
                    video = video + "?pltype" + m[1],
                    reg = /coverpic=(.+?)&/,
                    m = reg.exec(scripts[i].textContent),
                    coverImg = m[1];
                    break
                }
            }
            video && coverImg && (thumb.src = coverImg, thumb.width = 480, thumb.height = 360, thumb = encapsulateImage(thumb), thumb.container = _document.getElementById("flashArea"), thumb.video = video, thumb.media_type = 1, eImages.push(thumb))
        } else if (url.indexOf("www.yinyuetai.com") > 0) {
            var inDiv = _document.getElementById("postVideo").innerHTML,
            reg = /pic=(.+?)&/,
            m = reg.exec(inDiv);
            m && m[1] && (thumb.src = decodeURIComponent(m[1]), thumb.width = 480, thumb.height = 360, thumb = encapsulateImage(thumb), thumb.container = _document.getElementById("player"), thumb.video = _document.getElementById("flashCode").value, thumb.media_type = 1, eImages.push(thumb))
        } else if ((url.indexOf("www.iqiyi.com") > 0 || url.indexOf("yule.iqiyi.com") > 0) && info.hasOwnProperty("videoId")) thumb.src = "http://" + siteDomain + "/pins/create/video/qiyi/?id=" + info.videoId,
        thumb.width = 115,
        thumb.height = 77,
        thumb = encapsulateImage(thumb),
        thumb.container = _document.getElementById("flash"),
        thumb.video = "http://player.video.qiyi.com/" + info.videoId,
        thumb.media_type = 1,
        eImages.push(thumb);
        else if (url.indexOf("tv.sohu.com/201") > 0 && _document.getElementById("shareBtn")) thumb.src = cover,
        thumb.width = 480,
        thumb.height = 360,
        thumb = encapsulateImage(thumb),
        thumb.container = _document.getElementById("sohuplayer"),
        thumb.video = "http://share.vrs.sohu.com/" + vid + "/v.swf&autoplay=false",
        thumb.media_type = 1,
        eImages.push(thumb);
        else if (url.indexOf("my.tv.sohu.com") > 0) {
            var meta = _document.getElementsByTagName("meta");
            for (var i = 0; i < meta.length; i++) if (meta[i].getAttribute("property") == "og:image") {
                thumb.src = meta[i].getAttribute("content");
                break
            }
            thumb.width = 480,
            thumb.height = 360,
            thumb = encapsulateImage(thumb),
            thumb.container = _document.getElementById("sohuplayer"),
            thumb.video = "http://share.vrs.sohu.com/my/v.swf&topBar=1&id=" + _vid + "&autoplay=false",
            thumb.media_type = 1,
            eImages.push(thumb)
        } else if (url.indexOf("v.ku6.com") > 0) thumb.src = App.VideoInfo.data.data.bigpicpath,
        thumb.width = 480,
        thumb.height = 360,
        thumb = encapsulateImage(thumb),
        thumb.container = _document.getElementById("ku6player"),
        thumb.video = "http://player.ku6.com/refer/" + App.VideoInfo.id + "/v.swf",
        thumb.media_type = 1,
        eImages.push(thumb);
        else if (url.indexOf("v.youku.com") > 0) {
            var json = eval("(" + httpGet("http://v.youku.com/player/getPlayList/VideoIDS/" + videoId2) + ")");
            thumb.src = json.data[0].logo,
            thumb.width = 448,
            thumb.height = 336,
            thumb = encapsulateImage(thumb),
            thumb.container = _document.getElementById("player"),
            thumb.video = "http://player.youku.com/player.php/sid/" + videoId2 + "/v.swf",
            thumb.media_type = 1,
            eImages.push(thumb)
        } else if (url.indexOf("v.ifeng.com") > 0) {
            var a = url.split("/"),
            id = a[a.length - 1].split(".");
            id = id[0];
            var json = httpGet("http://v.ifeng.com/video_info_new/" + id[id.length - 2] + "/" + id[id.length - 2] + id[id.length - 1] + "/" + id + ".xml"),
            reg = /BigPosterUrl="(.+)" SmallPosterUrl/,
            a = reg.exec(json);
            thumb.src = a[1],
            thumb.width = 480,
            thumb.height = 360,
            thumb = encapsulateImage(thumb),
            thumb.container = _document.getElementById("playerDiv"),
            thumb.video = "http://v.ifeng.com/include/exterior.swf?guid=" + id + "&AutoPlay=false",
            thumb.media_type = 1,
            eImages.push(thumb)
        } else if (url.indexOf("www.56.com/u") > 0) {
            var reg = /v_(.+?)\.html/,
            a = reg.exec(url);
            a = a[1],
            thumb.src = "http://" + siteDomain + "/pins/create/video/56/?id=" + a,
            thumb.width = 480,
            thumb.height = 405,
            thumb = encapsulateImage(thumb),
            thumb.container = _document.getElementById("embed_flash_player"),
            thumb.video = "http://player.56.com/v_" + a + ".swf",
            thumb.media_type = 1,
            eImages.push(thumb)
        } else if (url.indexOf("www.jifenzhong.com/video") > 0 && _document.getElementById("flash_url")) {
            var json = httpGet("http://www.jifenzhong.com/playVideo.do?vid=" + _document.getElementById("shortCommentVideoId").value),
            reg = /<thumb_url>(.+)<\/thumb_url>/,
            a = reg.exec(json);
            thumb.src = a[1],
            thumb.width = 480,
            thumb.height = 305,
            thumb = encapsulateImage(thumb),
            thumb.container = _document.getElementById("JifenzhongPlayer"),
            thumb.video = _document.getElementById("flash_url").value,
            thumb.media_type = 1,
            eImages.push(thumb)
        } else if (url.indexOf("v.pptv.com/show") > 0) thumb.src = "http://" + siteDomain + "/pins/create/video/pptv/?id=" + webcfg.id,
        thumb.width = 120,
        thumb.height = 60,
        thumb = encapsulateImage(thumb),
        thumb.container = _document.getElementById("pptv_playpage_box"),
        thumb.video = webcfg.player.createConfig.playList[0].swf,
        thumb.media_type = 1,
        eImages.push(thumb);
        else if (url.indexOf("v.qq.com") > 0 && _document.getElementById("textfield2")) {
            var video = _document.getElementById("textfield2").value,
            reg = /vid=(.+)&/,
            a = reg.exec(video);
            thumb.src = "http://vpic.video.qq.com/76082551/" + a[1] + "_160_90_3.jpg",
            thumb.width = 160,
            thumb.height = 90,
            thumb = encapsulateImage(thumb),
            thumb.container = _document.getElementById("mod_player"),
            thumb.video = video,
            thumb.media_type = 1,
            eImages.push(thumb)
        }
        var iframes = _document.getElementsByTagName("iframe");
        for (var i = 0; i < iframes.length; i++) try {
            var d = iframes[i].contentDocument;
            if (d) {
                var parentNode = iframes[i].parentNode;
                eImages = getCurrentPageImagesWithEncapsulation(d, eImages, {
                    parentNode: parentNode
                })
            }
        } catch(e) {}
        return eImages
    }
    function httpGet(e) {
        var t = null;
        return t = new XMLHttpRequest,
        t.open("GET", e, !1),
        t.send(null),
        t.responseText
    }
    function getSelectedText() {
        return ("" + (window.getSelection ? window.getSelection() : document.getSelection ? document.getSelection() : document.selection.createRange().text)).replace(/(^\s+|\s+$)/g, "")
    }
    function isIE() {
        return /msie/i.test(navigator.userAgent) && !/opera/i.test(navigator.userAgent)
    }
    function isSafari() {
        return /Safari/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent)
    }
    function isPinable(e) {
        var t = !0,
        n = !1,
        r = this.location,
        i = r.host;
        if (/^(?:about|chrome)/.test(r.protocol)) r.href = "http://" + siteDomain,
        t = !1;
        else if (siteDomain == i) / ^\ / guide\ / pin\ / ?/.test(r.pathname)||(e&&alert("浣犲氨鍦ㄨ姳鐡ｆ湰绔欏憿锛屼笉鑳介噰闆嗘湰绔欏浘鐗囥€�"),t=!1);else if(/ ^ 127.0.0.1( ? ::\d + ) ? /.test(i))n=!0;else if(/ ^ localhost( ? ::\d + ) ? /.test(i))n=!0;else if(/ ^ 10\. / .test(i)) n = !0;
        else if (/^192\.168\./.test(i)) n = !0;
        else if (/^(?:\d+\.){3}\d+$/.test(i)) {
            var s = i.split("."),
            o = parseInt(s[0], 10),
            s = parseInt(s[1], 10);
            o === 172 && s > 15 && s < 32 ? n = !0 : o === 169 && s === 254 && (n = !0)
        }
        return n && (e && alert("浣犵幇鍦ㄨ闂殑鏄唴閮ㄧ綉缁滐紝涓嶈兘閲囬泦鍐呯綉鍥剧墖銆�"), t = !1),
        t
    }
    function pinImage(e, t) {
        for (i in filters) {
            var n = new RegExp(i);
            if (n.test(location.href)) {
                e = filters[i](e) || e;
                break
            }
        }
        var r = e.url || (e.src == location.href ? document.referrer || location.href: location.href),
        s = e.img,
        o = s.src.match("^https?://(.*?)/");
        o = o[1],
        o.indexOf("taobaocdn.com") > -1 && (s.src = s.src.replace(/_310x310.jpg/, "")),
        isSafari() && (r = encodeURI(r));
        var u = e.big_img ? e.big_img: s,
        a = {
            media: e.big_img ? e.big_img.src: s.src,
            url: r,
            w: u.naturalWidth || u.width,
            h: u.naturalHeight || u.height,
            alt: s.alt,
            title: e.title || document.title,
            description: e.description || "",
            media_type: e.media_type || "",
            video: e.video || ""
        };
        imageDesc = getSelectedText() || selectedText,
        imageDesc && (a.description = imageDesc);
        var f = [];
        f.push(bookmarkletUrl),
        f.push("?");
        if (t && typeof t == "function") return t(a);
        for (var l in a) f.push(encodeURIComponent(l)),
        f.push("="),
        f.push(encodeURIComponent(a[l])),
        f.push("&");
        isShareBtn && f.push("is_share_btn=1&"),
        huaban_md && f.push("md=" + encodeURIComponent(huaban_md));
        var r = f.join(""),
        c = "status=no,resizable=no,scrollbars=yes,personalbar=no,directories=no,location=no,toolbar=no,menubar=no,width=632,height=320,left=0,top=0";
        window.open(r, "pin" + (new Date).getTime(), c)
    }
    function thunderpinImage(e, t, n) {
        if (Browser.ie6 || Browser.ie7) return window.alert("鎮ㄧ殑娴忚鍣ㄧ増鏈お浣庯紝璇峰崌绾т綘鐨勬祻瑙堝櫒銆�");
        if (!isLogin) {
            var r = "http://" + siteDomain + "/login/?dialog=1&next=" + encodeURIComponent("/logined.html"),
            i = "status=no,resizable=no,scrollbars=yes,personalbar=no,directories=no,location=no,toolbar=no,menubar=no,width=632,height=320,left=0,top=0",
            s = window.open(r, "login" + (new Date).getTime(), i),
            o = setInterval(function() {
                try {
                    s.closed && (clearInterval(o), checkLogin())
                } catch(e) {}
            },
            1e3);
            return ! 1
        }
        return pinImage(e,
        function(r) {
            if (thunderpin_state(e, t, n, "ing")) return ! 1;
            var i = {
                text: r.description || r.title || r.alt || "",
                link: r.url || "",
                img_url: r.media,
                media_type: r.media_type,
                video: r.video || "",
                is_share_btn: isShareBtn ? 1 : "",
                check: !0
            },
            s = function(r) {
                if (r.err) return thunderpin_state(e, t, n, "failed", r.msg);
                if (r.warning == 100) {
                    var u = function() {
                        delete i.check,
                        xdm && xdm.request && xdm.request({
                            url: "/pins/",
                            data: i,
                            noCache: !0,
                            method: "post"
                        },
                        s, o)
                    },
                    a = "浣犲凡缁忓湪鐢绘澘" + r.pin.board.title + "涓噰闆嗚繃杩欏紶鍥剧墖";
                    return thunderpin_state(e, t, n, "warning", a, u)
                }
                var a = '<a href="http://' + siteDomain + "/pins/" + r.pin.pin_id + '/" target="_blank;">鏌ョ湅閲囬泦</a>';
                return thunderpin_state(e, t, n, "success", a)
            },
            o = function() {
                thunderpin_state(e, t, n, "failed")
            };
            xdm && xdm.request && xdm.request({
                url: "/pins/",
                data: i,
                noCache: !0,
                method: "post"
            },
            s, o)
        }),
        !1
    }
    function thunderpin_state(e, t, n, r, i, s) {
        function d() {
            if (r == "success" || r == "failed") a = setTimeout(function() {
                o.setAttribute("data-thunder", ""),
                f && f.parentNode && f.parentNode.removeChild(f)
            },
            3e3)
        }
        var o = e.container || e.img,
        u = o.getAttribute("data-thunder");
        if (r == "ing" && u) return ! 0;
        var a, f;
        if (!u) {
            u = Math.floor(new Date / 1e3),
            o.setAttribute("data-thunder", u),
            f = generateTag((t ? "p_": "") + u),
            t ? t.appendChild(f) : document.body.appendChild(f),
            isIE() ? f.className = global + "_thunder_tip" + " " + global + "_thunder_tip_" + r: f.setAttribute("class", global + "_thunder_tip" + " " + global + "_thunder_tip_" + r),
            i = i || "";
            var l = r == "success" ? "閲囬泦鎴愬姛锛�": r == "ing" ? "閲囬泦涓€�": "閲囬泦澶辫触锛�";
            if (r == "warning") {
                var c = generateTag("thunder_pin_operations", "p"),
                h = generateTag("continue_thunder_pin", "a");
                h.href = "javascirpt:;",
                h.appendChild(document.createTextNode("缁х画")),
                h.onclick = function() {
                    return s(),
                    !1
                };
                var p = generateTag("cannel_thunder_pin", "a");
                p.href = "javascript:;",
                p.appendChild(document.createTextNode("鍙栨秷")),
                p.onclick = function() {
                    o.setAttribute("data-thunder", ""),
                    f && f.parentNode && f.parentNode.removeChild(f)
                },
                f.innerHTML = "<span><em></em>" + i + "</span>",
                c.appendChild(h),
                c.appendChild(document.createTextNode("锛屾垨鑰�")),
                c.appendChild(p),
                f.appendChild(c)
            } else f.innerHTML = "<span><em></em>" + l + "</span><p>" + i + "</p>";
            if (!t) {
                f.style.top = n.top,
                f.style.left = n.left;
                if (r == "success" || r == "failed") f.style.top = parseInt(n.top) - 16 + "px"
            }
            return f.onmouseover = function() {
                clearTimeout(a)
            },
            f.onmouseout = function() {
                d()
            },
            d(),
            !1
        }
        return setTimeout(function() {
            f = document.getElementById(global + "_" + (t ? "p_": "") + u),
            o.setAttribute("data-thunder", ""),
            f && f.parentNode && f.parentNode.removeChild(f),
            thunderpin_state(e, t, n, r, i, s)
        },
        500)
    }
    function hideTips() {
        var e = __getElements(document.body, "." + global + "_thunder_tip");
        for (var t = 0; t < e.length; t += 1) e[t].style.display = "none"
    }
    function showImages(e) {
        if (showingImage) return;
        hideTips(),
        lastScrollY = window.pageYOffset || document.body.scrollTop;
        var t = function() {
            return n.parentNode.removeChild(n),
            r.parentNode.removeChild(r),
            showingImage = !1,
            selectedText = "",
            window.scroll(0, lastScrollY),
            !1
        },
        n = generateTag("Overlay");
        document.keydown = t,
        document.body.appendChild(n),
        isIE() && (n.style.width = document.body.clientWidth + "px", n.style.height = document.body.clientHeight + "px");
        var r = generateTag("Container");
        document.body.appendChild(r);
        var i = document.createElement("div");
        i.setAttribute("id", global + "_Control");
        var s = new Image;
        s.src = imageRoot + "/LogoAbout.png",
        i.appendChild(s);
        var o = generateTag("RemoveLink", "a");
        o.href = "javascirpt:;",
        o.appendChild(document.createTextNode("鍙栨秷")),
        i.appendChild(o),
        r.appendChild(i),
        document.getElementById(global + "_RemoveLink").onclick = t;
        var u = {};
        for (var a = 0; a < e.length; a++) u[e[a].src] || (u[e[a].src] = 1,
        function(e) {
            var n, r = document.createElement("div");
            isIE() ? r.className = global + "ImagePreview": r.setAttribute("class", global + "ImagePreview");
            var i = document.createElement("div");
            isIE() ? i.className = global + "Img": i.setAttribute("class", global + "Img");
            var s = document.createElement("span");
            s.innerHTML = e.w + " x " + e.h,
            isIE() ? s.className = global + "Dimensions": s.setAttribute("class", global + "Dimensions"),
            r.appendChild(s),
            document.getElementById(global + "_Container").appendChild(r).appendChild(i),
            n = document.createElement("a"),
            n.setAttribute("href", "javascript:;");
            if (e.video) {
                var o = document.createElement("span");
                isIE() ? o.className = global + "VideoIcon": o.setAttribute("class", global + "VideoIcon"),
                n.appendChild(o)
            }
            i.appendChild(n);
            var u = document.createElement("img");
            isIE() ? i.className = global + "Img": i.setAttribute("class", global + "Img"),
            u.style["margin-top"] = calculateMarginTop(e),
            u.src = e.src,
            u.setAttribute("alt", "Pin This"),
            u.className = "ImageToPin",
            n.appendChild(u);
            var a = document.createElement("strong"),
            f = document.createElement("strong");
            isIE() ? (a.className = global + "_ThunderPin", f.className = global + "_Pin") : (a.setAttribute("class", global + "_ThunderPin"), f.setAttribute("class", global + "_Pin")),
            a.setAttribute("title", "蹇€熼噰闆�"),
            f.setAttribute("title", "閲囬泦鍒拌姳鐡�"),
            a.onclick = function() {
                thunderpinImage(e, r);
                return
            },
            f.onclick = function() {
                return pinImage(e),
                t()
            },
            isIE() ? (n.attachEvent("onmouseover",
            function() {
                a.style.display = "block",
                f.style.display = "block"
            }), n.attachEvent("onmouseout",
            function() {
                a.style.display = "none",
                f.style.display = "none"
            })) : (n.addEventListener("mouseover",
            function() {
                a.style.display = "block",
                f.style.display = "block"
            },
            !1), n.addEventListener("mouseout",
            function() {
                a.style.display = "none",
                f.style.display = "none"
            },
            !1)),
            n.appendChild(a),
            n.appendChild(f)
        } (e[a]));
        showingImage = !0
    }
    function initPinBtn(e) {
        generatePinBtn(),
        registerImagesForPinBtn(e)
    }
    function showImagesAndInitPinBtn() {
        if (!isPinable(!0)) return;
        var e = getCurrentPageImagesWithEncapsulation();
        imageDesc = getSelectedText() || selectedText;
        if (e.length == 0) {
            if (!reported) {
                reported = !0;
                var t = location.href,
                n = new Image;
                n.src = "http://" + siteDomain + "/feedback/objnotfound?link=" + encodeURIComponent(t)
            }
            try {
                window.top === window.self && window.alert("鎶辨瓑锛岄〉闈�笂娌℃湁瓒冲澶х殑鍥剧墖銆�")
            } catch(r) {}
        } else showImages(e),
        initPinBtn(e),
        window.scroll(0, 0)
    }
    function getToggleOn(e) {
        e(!0)
    }
    function showFlash() {
        var e = document.getElementById(global + "_FixFlashStyle");
        e && (document.getElementsByTagName("head")[0] || document.body).removeChild(e)
    }
    function hideFlash() {
        var e = global + "_FixFlashStyle";
        if (!document.getElementById(e)) {
            var t = "object, embed {visibility: hidden; display:none;}",
            n = document.createElement("style");
            n.id = e,
            (document.getElementsByTagName("head")[0] || document.body).appendChild(n),
            n.styleSheet ? n.styleSheet.cssText = t: n.appendChild(document.createTextNode(t))
        }
    }
    function initParams() {
        w = window.huaban_minWidth || minWidth,
        h = window.huaban_minHeight || minHeight,
        minWidth = w < minWidth ? minWidth: w,
        minHeight = h < minHeight ? minHeight: h,
        huaban_md = window.huaban_md || "";
        if (isShareBtn && !huaban_md) {
            var e = location && location.host && location.host.split(".") || [];
            e[0] == "www" && e.shift(),
            e.length && (huaban_md = e.join("."))
        }
    }
    function checkLogin() {
        xdm && xdm.request && xdm.request({
            url: "/users/me/",
            noCache: !0
        },
        function(e) {
            e.err || (isLogin = !0)
        },
        function() {})
    }
    function initXDM() {
        xdm = new easyXDM.Rpc({
            swf: "http://" + siteDomain + "/js/lib/easyxdm.swf",
            remote: "http://" + siteDomain + "/xdm/",
            remoteHelper: "http://" + siteDomain + "/name.html",
            onReady: function() {
                checkLogin()
            }
        },
        {
            remote: {
                request: {}
            }
        })
    }
    function loadJSON(e) {
        var t = document.createElement("script");
        t.type = "text/javascript",
        t.src = json2Url,
        t.onreadystatechange = function() { (this.readyState === "complete" || this.readyState === "loaded") && e()
        },
        t.onload = e;
        var n = window.document.getElementsByTagName("head")[0] || window.document.body;
        n.appendChild(t)
    }
    var global = "huaban",
    old_global = "__huaban";
    document[global] = document[global] || {},
    document[old_global] = document[global];
    var minWidth = 100,
    minHeight = 100,
    huaban_md = "",
    siteDomain = "huaban.com",
    imageRoot = "http://" + siteDomain + "/img",
    bookmarkletUrl = "http://" + siteDomain + "/bookmarklet/",
    analyticsUrl = "http://" + siteDomain + "/share_analytics.html",
    xdmUrl = "http://" + siteDomain + "/js/lib/easyXDM.min.js",
    json2Url = "http://" + siteDomain + "/js/lib/json2.js",
    domChanged = !1,
    selectedText = "",
    lastScrollY = 0,
    isShareBtn = !1,
    isLogin = !1,
    btnPositions = ["top", "left"],
    pinBtn = null,
    thunderpinBtn = null,
    hidePinBtnTimer = null,
    xdm,
    currentImage = null,
    imageDesc = "",
    showingImage = !1,
    itemUrl = "",
    skip = !1,
    skiphrefs = ["http://www.diandian.com/wall"]; (function() {
        for (var e = 0; e < skiphrefs.length; e++) if (location.href.indexOf(skiphrefs[e]) >= 0) {
            skip = !0;
            break
        }
    })();
    var important = !1,
    importantCssWebsites = ["faxianla.com"]; (function() {
        for (var e = 0; e < importantCssWebsites.length; e++) if (location.href.indexOf(importantCssWebsites[e]) >= 0) {
            important = !0;
            break
        }
    })();
    var Browser = function() {
        var e = "modernizr",
        t = document.createElement(e),
        n = t.style,
        r = function() {
            var e = "Webkit Moz O ms Khtml".split(" "),
            t = "transitionProperty",
            r = t.charAt(0).toUpperCase() + t.substr(1),
            i = (t + " " + e.join(r + " ") + r).split(" "),
            s = !1;
            for (var o in i) if (n[i[o]] !== undefined) {
                s = !0;
                break
            }
            return s
        },
        i = {
            ie: !1,
            ie6: !1,
            ie7: !1,
            ie8: !1,
            ie9: !1,
            chrome: !1,
            firefox: !1,
            opera: !1
        },
        s = navigator.userAgent.toLowerCase(),
        o = navigator.platform.toLowerCase(),
        u = s.match(/(opera|ie|firefox|chrome|version)[\s\/:]([\w\d\.]+)?.*?(safari|version[\s\/:]([\w\d\.]+)|$)/) || [null, "unknown", 0],
        a = u[1] == "ie" && document.documentMode,
        f = u[1] == "version" ? u[3] : u[1];
        return i.version = a || parseFloat(u[1] == "opera" && u[4] ? u[4] : u[2]),
        i[f] = !0,
        i[f + parseInt(i.version, 10)] = !0,
        i
    } (),
    checkbgimgs = function(e) {
        var t = e;
        if (!t) return;
        var n = t.style.backgroundImage || t.style.getPropertyValue && t.style.getPropertyValue("background-image");
        if (!n) return;
        var r = n.match(/url\((.+)\)/);
        if (r == null || r.length != 2) return;
        var i = r[1];
        if (i.indexOf("http://") == 0 || i.indexOf("https://") == 0 || i.indexOf("/") == 0) {
            var s = new Image;
            s.src = i;
            var o = {
                container: t,
                w: s.naturalWidth || s.width,
                h: s.naturalHeight || s.height,
                src: s.src,
                img: s,
                alt: "",
                img2: s
            };
            return o
        }
        return
    },
    bgimgs = {
        "^http://1x\\.com/": function() {
            var e = checkbgimgs(document.getElementById("bigimage2"));
            if (e) return [e];
            return
        },
        "^http://\\w+\\.163\\.com/photoview/": function() {
            var e = document.getElementById("modePhoto");
            if (!e) return;
            var t = __getElement(e, "#photoView img"),
            n = __getElement(e, ".nph_photo_prev"),
            r = __getElement(e, "#photoDesc"),
            i = document.title || "";
            i += "\n";
            if (t && n) return [{
                container: n,
                w: t.naturalWidth || t.width,
                h: t.naturalHeight || t.height,
                src: t.src,
                img: t,
                description: i + (r && r.innerText || ""),
                img2: t
            }];
            return
        },
        "^http://luxury\\.qq\\.com/": function() {
            var e = document.getElementById("Main-A"),
            t = document.getElementById("mainArea"),
            n,
            r,
            i,
            s = document.title || "";
            e && (n = __getElement(e, "#PicSrc"), r = __getElement(e, "#mouseOverleft"), i = __getElement(document.body, "#Main-B > p"), i && (i = i.innerText || "")),
            t && (n = document.getElementById("Display"), r = document.getElementById("preArrow"), i = __getElement(t, "#titleArea > p"), i && (i = i.innerText || "")),
            s += "\n";
            if (n && r) return [{
                container: r,
                w: n.naturalWidth || n.width,
                h: n.naturalHeight || n.height,
                src: n.src,
                img: n,
                description: s + i,
                img2: n
            }];
            return
        },
        "^http(s)?://slide\\.news\\.sina\\.com\\.cn/": function() {
            var e = document.getElementById("efpBigPic"),
            t = document.getElementById("efpTxt");
            if (!e) return;
            var n = __getElement(e, "#d_BigPic img"),
            r = __getElement(e, "#efpLeftArea"),
            i = t && __getElement(t, "#efpTxt > #d_picIntro") || "",
            s = document.getElementById("d_picTit");
            s = s ? s.innerHTML: document.title || "",
            i = i ? i.innerHTML: "";
            if (n && r) return [{
                container: r,
                w: n.naturalWidth || n.width,
                h: n.naturalHeight || n.height,
                src: n.src,
                img: n,
                description: (s + "\n" + i).trim(),
                img2: n
            }];
            return
        },
        "^http://\\w+\\.flickr\\.com/": function() {
            var e = document.getElementById("photo");
            if (!e) return;
            var t = __getElement(e, "img"),
            n = __getElement(e, "#photo-drag-proxy"),
            r = document.title || "",
            i = [];
            t && n && i.push({
                container: n,
                w: t.width,
                h: t.height,
                src: t.src,
                img: t,
                description: r.trim(),
                img2: t
            }),
            e = document.getElementById("lightbox");
            if (e) {
                var s = __getElements(e, "li");
                for (var o = 0; o < s.length; o++) {
                    var u = s[o];
                    t = __getElement(u, "img.loaded"),
                    n = __getElement(u, "span.facade-of-protection"),
                    t && n && i.push({
                        container: n,
                        w: t.width,
                        h: t.height,
                        src: t.src,
                        img: t,
                        description: r.trim(),
                        img2: t
                    })
                }
            }
            return i
        }
    },
    filters = {
        "^http(s)?://(\\w+\\.)?diandian\\.com": function(e) {
            var t = e.img,
            n = null,
            r = null,
            i = null;
            if (tagName(t) == "img") {
                t = t.parentNode;
                var s = !1;
                while (t && t.nodeName.toLowerCase() != "body") {
                    var o = getClass(t);
                    if (o == "feed-content-holder pop") {
                        var u = __getElement(t, "div.link-to-post-holder a.link-to-post");
                        u && (n = u.getAttribute("href"), s = !0);
                        var a = __getElement(t, "div.feed-ct");
                        a && (i = a.innerText || a.textContent || "", i = i.trim())
                    } else if (o = tagName(t) == "a") n = t.getAttribute("href"),
                    s = !0;
                    if (s) break;
                    t = t.parentNode || null
                }
            }
            return n && (e.url = getHref(n)),
            r && (e.title = r),
            i && (e.description = i),
            e
        },
        "^http://(.*\\.)?weibo\\.com": function(e) {
            var t = e.img,
            n = null,
            r = null,
            i = null;
            if (tagName(t) == "img" && getAttribute(t, "action-type") == "feed_list_media_bigimg") {
                t = t.parentNode;
                var s = !1;
                while (t && t.nodeName.toLowerCase() != "body" && (tagName(t) != "dl" || !hasClass(t, "feed_list"))) {
                    if (tagName(t) == "dd" && hasClass(t, "content")) {
                        s = !0;
                        var o = __getElement(t, "a[node-type=feed_list_item_date]");
                        o && (n = o.getAttribute("href") || "");
                        var u = __getElement(t, "p[node-type=feed_list_content]");
                        u && (i = u.innerText || u.textContent || "", i = i.trim())
                    } else if (tagName(t) == "div" && hasClass(t, "WB_detail")) {
                        s = !0;
                        var a, f = __getElements(t, "div.WB_func");
                        for (var l = 0; l < f.length; l++) {
                            var c = f[l].parentNode;
                            tagName(c) == "div" && hasClass(c, "WB_detail") && (a = f[l])
                        }
                        if (a) {
                            var o = __getElement(a, "a[node-type=feed_list_item_date]");
                            o && (n = o.getAttribute("href") || "");
                            var u = __getElement(t, "div[node-type=feed_list_content]");
                            u && (i = u.innerText || u.textContent || "", i = i.trim())
                        }
                    }
                    if (s) break;
                    t = t.parentNode || null
                }
            } else if (tagName(t) == "img" && getAttribute(t, "node-type") == "feed_list_media_bgimg") {
                t = t.parentNode;
                var s = !1;
                while (t && t.nodeName.toLowerCase() != "body" && (tagName(t) != "dl" || !hasClass(t, "feed_list"))) {
                    if (tagName(t) == "div" && hasClass(t, "WB_detail")) {
                        s = !0;
                        var a, f = __getElements(t, "div.WB_func");
                        for (var l = 0; l < f.length; l++) {
                            var c = f[l].parentNode;
                            tagName(c) == "div" && hasClass(c, "WB_detail") && (a = f[l])
                        }
                        if (a) {
                            var o = __getElement(a, "a[node-type=feed_list_item_date]");
                            o && (n = o.getAttribute("href") || "");
                            var u = __getElement(t, "div[node-type=feed_list_content]");
                            u && (i = u.innerText || u.textContent || "", i = i.trim())
                        }
                    }
                    if (s) break;
                    t = t.parentNode || null
                }
            } else if (tagName(t) == "img" && getAttribute(t, "node-type") == "img_view") {
                t = t.parentNode && t.parentNode.parentNode || null;
                if (t && hasClass(t, "big_pic") && getAttribute(t, "node-type") == "layer_center") {
                    var o = __getElement(t, "p[node-type=feed_list_content] a[node-type=feed_list_item_date]");
                    o && (n = o.getAttribute("href") || "");
                    var u = __getElement(t, "p[node-type=feed_list_content]");
                    u && (i = u.innerText || u.textContent || "", i = i.trim())
                }
            } else if (tagName(t) == "img" && t.parentNode && t.parentNode.parentNode && t.parentNode.parentNode.parentNode && getAttribute(t.parentNode.parentNode.parentNode, "node-type") == "albumDetail") {
                var h = t.parentNode.parentNode.parentNode,
                o = tagName(t.parentNode) == "a" ? t.parentNode: !1;
                o && (n = o.getAttribute("href") || "");
                var u = h && __getElement(h, ".photo_comment > div > p");
                u && (i = u.innerText || u.textContent || "", i = i.trim())
            }
            if (e.container && (tagName(e.container) == "embed" || tagName(e.container) == "object")) {
                t = e.container;
                var s = !1;
                while (tagName(t) != "body") {
                    if (getAttribute(t, "node-type") == "feed_list_media_bigvideoDiv" || getAttribute(t, "note-type") == "feed_list_media_bigvideoDiv") {
                        t = t.parentNode && t.parentNode.parentNode && t.parentNode.parentNode.parentNode,
                        s = !0;
                        if (!t) break;
                        var o = __getElement(t, "p[node-type=feed_list_content]~p a[node-type=feed_list_item_date]");
                        o ? n = o.getAttribute("href") || "": (o = __getElement(t, "div[node-type=feed_list_reason]~div a[node-type=feed_list_item_date]"), o || (o = __getElement(t, "div[node-type=feed_list_content]~div a[node-type=feed_list_item_date]")), o && (n = "http://weibo.com" + o.getAttribute("href") || ""));
                        var u = __getElement(t, "p[node-type=feed_list_content]");
                        u || (u = __getElement(t, "div[node-type=feed_list_reason]")),
                        u || (u = __getElement(t, "div[node-type=feed_list_content]")),
                        u && (i = u.innerText || u.textContent || "", i = i.trim())
                    }
                    if (s) break;
                    t = t.parentNode || null
                }
            }
            return n && (e.url = getHref(n)),
            r && (e.title = r),
            i && (e.description = i),
            e
        },
        "^http(s)?://www\\.google\\.com/reader/": function(e) {
            var t = e.img,
            n = null,
            r = null,
            i = null;
            if (tagName(t) == "img") {
                t = t.parentNode;
                var s = !1;
                while (t && t.nodeName.toLowerCase() != "body" && (tagName(t) != "div" || !hasClass(t, "entry-container"))) {
                    if (tagName(t) == "div" && hasClass(t, "entry-main")) {
                        s = !0;
                        var o = __getElement(t, "h2.entry-title a.entry-title-link");
                        o && (n = o.getAttribute("href") || "", r = o.innerText || o.textContent || "", r = r.trim(), i = r)
                    }
                    if (s) break;
                    t = t.parentNode || null
                }
            }
            n && (e.url = getHref(n)),
            i && (e.title = i),
            r && (e.description = r)
        },
        "^http(s)?://(www\\.)?(markzhi|faxianla)\\.com": function(e) {
            var t = e.img,
            n = null,
            r = null,
            i = null,
            s = null;
            if (tagName(t) == "img" && t.parentNode && t.parentNode.parentNode && hasClass(t.parentNode.parentNode, "item mark")) {
                var o = getAttribute(t, "src");
                o && /metal.jpg$/.test(o) && (s = o.replace(/metal.jpg$/, "wood.jpg")),
                o && /\/metal\//.test(o) && (s = o.replace(/\/metal\//, "/wood/")),
                t = t.parentNode;
                var u = null;
                tagName(t) == "a" && hasClass(t, "image") && (n = getAttribute(t, "href")),
                t = t.parentNode;
                var a = __getElement(t, "strong.title");
                a && (i = a.innerText || a.textContent || "", i = i.trim())
            }
            n && (e.url = getHref(n)),
            i && (e.title = i),
            r && (e.description = r);
            if (s) {
                var f = new Image;
                f.alt = e.img.alt,
                f.src = s,
                e.big_img = f
            }
        },
        "^http(s)?://plus\\.google\\.com/": function(e) {
            var t = e.img,
            n = null;
            itemUrl && (n = itemUrl);
            if (t.parentNode) {
                var r = getAttribute(t.parentNode, "data-content-url");
                r && /http(s)?:\/\/plus.google.com\/photos\/.+\/albums\/.+/.test(r) && (n = r)
            }
            n && (e.url = getHref(n))
        },
        "^http(s)?://(www\\.)?tumblr\\.com": function(e) {
            var t = e.img,
            n = null,
            r = null;
            if (tagName(t) == "img") {
                t = t.parentNode;
                var i = !1;
                while (t && t.nodeName.toLowerCase() != "body") {
                    if (tagName(t) == "li" && hasClass(t, "post") && t.id && t.id.indexOf("post_") == 0) {
                        i = !0;
                        var s = __getElement(t, "a.permalink");
                        s && (n = s.getAttribute("href") || "");
                        var o = __getElement(t, "div.caption > p");
                        o && (r = o.innerText || o.textContent || "", r = r.trim())
                    }
                    if (i) break;
                    t = t.parentNode || null
                }
            }
            n && (e.url = getHref(n)),
            r && (e.description = r)
        },
        "^http(s)?://(www\\.)?topit\\.me": function(e) {
            var t = e.img,
            n = null,
            r = null,
            i = null;
            if (tagName(t) == "img") {
                t = t.parentNode;
                var s = !1;
                while (t && t.nodeName.toLowerCase() != "body") {
                    if (tagName(t) == "div" && hasClass(t, "e") && hasClass(t, "m")) {
                        s = !0;
                        var o = e.img.parentNode;
                        n = o.getAttribute("href") || "";
                        var u = __getElement(t, ".bar > .title");
                        r = u && u.innerText || u.textContent || "",
                        u = __getElement(t, ".bar > .info"),
                        r = u && r && r.trim() + "\n",
                        r += u && u.innerText || u.textContent || "",
                        r = r.trim();
                        var a = getAttribute(e.img, "src");
                        a && (/m\.jpg$/.test(a) ? i = a.replace(/m\.jpg$/, "l.jpg") : /topit\.me\/m\d+\//.test(a) ? i = a.replace(/(topit\.me\/)m(\d+\/)/, "$1l$2") : /img\.topit\.me\/m\//.test(a) && (i = a.replace(/(img\.topit\.me\/)m(\/)/, "$1l$2")))
                    }
                    if (s) break;
                    t = t.parentNode || null
                }
            }
            n && (e.url = getHref(n)),
            r && (e.description = r);
            if (i) {
                var f = new Image;
                f.alt = e.img.alt,
                f.src = i,
                e.big_img = f
            }
        },
        "^http(s)?://(www.)?woxihuan.com/": function(e) {
            var t = e.img,
            n = null,
            r = null,
            i = null,
            s = null;
            if (tagName(t) == "img" && t.parentNode && t.parentNode.parentNode && t.parentNode.parentNode.parentNode && hasClass(t.parentNode.parentNode.parentNode, "cellItem")) {
                var o = getAttribute(t, "src");
                o && /\/196__\//.test(o) && (s = o.replace(/\/196__\//, "/680__/")),
                t = t.parentNode;
                var u = null;
                tagName(t) == "a" && getAttribute(t, "module-tag") && (n = getAttribute(t, "href")),
                t = t.parentNode.parentNode;
                var a = __getElement(t, "h3 span.cellTit");
                a && (i = a.innerText || a.textContent || "", i = i.trim())
            }
            n && (e.url = getHref(n)),
            i && (e.title = i),
            r && (e.description = r);
            if (s) {
                var f = new Image;
                f.alt = e.img.alt,
                f.src = s,
                e.big_img = f
            }
        }
    },
    isShowedBtn = !1,
    reported = !1; (function() {
        if (document[global]._loaded) return;
        if (isPinable(!1)) {
            generateStyleElement();
            if (document.getElementById("huaban_script")) showImagesAndInitPinBtn();
            else if (document.getElementById("huaban_user_script") || document.getElementById("huaban_share_script")) {
                if (document.getElementById("huaban_share_script")) {
                    isShareBtn = !0;
                    var e = document.getElementById("huaban_share_script").getAttribute("data-position") || "";
                    btnPositions = e.split(" "),
                    initParams()
                }
                var t = getCurrentPageImagesWithEncapsulation();
                t.length > 0 && initPinBtn(t)
            } else showImagesAndInitPinBtn()
        }
        isIE() || (document.body.addEventListener("DOMNodeInserted",
        function(e) {
            domChanged = !0,
            clearTimeout(n),
            n = setTimeout(r, 500)
        },
        !1), window.addEventListener("scroll",
        function() {
            domChanged = !0,
            clearTimeout(n),
            n = setTimeout(r, 500)
        },
        !1));
        var n = !1,
        r = function() {
            if (!domChanged) return;
            var e = getCurrentPageImagesWithEncapsulation();
            e.length > 0 && initPinBtn(e),
            domChanged = !1,
            n = setTimeout(r, 5e3)
        };
        setTimeout(r, 5e3),
        isIE() ? document.body.attachEvent("onclick",
        function() {
            var e = window.event;
            if (e.target && e.target.tagName == "pinit") return;
            domChanged = !0,
            clearTimeout(n),
            n = setTimeout(r, 500)
        }) : document.body.addEventListener("click",
        function(e) {
            if (e.target && e.target.tagName == "pinit") return;
            e.target && tagName(e.target) == "img" && e.target.parentNode && (itemUrl = getAttribute(e.target.parentNode, "data-content-url")),
            domChanged = !0,
            clearTimeout(n),
            n = setTimeout(r, 500)
        });
        if (isShareBtn) try {
            var i = document.createElement("iframe");
            i.setAttribute("src", analyticsUrl),
            i.style.width = "0px",
            i.style.height = "0px",
            i.style.display = "none",
            window.document.body.appendChild(i)
        } catch(s) {} else {
            var o = function() {
                var e = document.createElement("script");
                e.type = "text/javascript",
                e.src = xdmUrl,
                e.onreadystatechange = function() { (this.readyState === "complete" || this.readyState === "loaded") && initXDM()
                },
                e.onload = initXDM;
                var t = window.document.getElementsByTagName("head")[0] || window.document.body;
                t.appendChild(e)
            };
            isIE() ? loadJSON(o) : o()
        }
        document[global]._loaded = !0,
        document[global].showValidImages = showImagesAndInitPinBtn,
        document[old_global]._loaded = document[global]._loaded,
        document[old_global].showValidImages = document[global].showValidImages
    })()
} ();