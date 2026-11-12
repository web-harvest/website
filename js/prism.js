/* Prism.js - Lightweight, extensible syntax highlighter */

(function (Prism) {
    'use strict';

    // XML language definition
    Prism.languages.xml = Prism.languages.markup = {
        'comment': /<!--[\s\S]*?-->/,
        'prolog': /<\?[\s\S]+?\?>/,
        'doctype': {
            pattern: /<!DOCTYPE(?:[^>"'[\]]|"[^"]*"|'[^']*')+(?:\[(?:[^<"'\]]|"[^"]*"|'[^']*'|<(?!!--)|<!--(?:[^-]|-(?!->))*-->)*\]\s*)?>/i,
            greedy: true,
            inside: {
                'internal-subset': {
                    pattern: /(\[)[\s\S]+(?=\])/,
                    lookbehind: true,
                    inside: null // see below
                },
                'string': {
                    pattern: /"[^"]*"|'[^']*'/,
                    greedy: true
                },
                'punctuation': /^<!|>$|[[\]]/,
                'doctype-tag': /^DOCTYPE/i,
                'name': /[^\s<>'"]+/
            }
        },
        'cdata': /<!\[CDATA\[[\s\S]*?\]\]>/i,
        'tag': {
            pattern: /<\/?(?!\d)[^\s>\/=$<%]+(?:\s(?:\s*[^\s>\/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+(?=[\s>]))|(?:\s|$)))*)?\s*\/?>/,
            greedy: true,
            inside: {
                'tag': {
                    pattern: /^<\/?[^\s>\/]+/,
                    inside: {
                        'punctuation': /^<\/?/,
                        'namespace': /^[^\s>\/:]+:/
                    }
                },
                'attr-value': {
                    pattern: /=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+)/,
                    inside: {
                        'punctuation': [
                            /^=/,
                            {
                                pattern: /^(\s*)["']|["']$/,
                                lookbehind: true
                            }
                        ]
                    }
                },
                'punctuation': /\/?>/,
                'attr-name': {
                    pattern: /[^\s>\/]+/,
                    inside: {
                        'namespace': /^[^\s>\/:]+:/
                    }
                }
            }
        },
        'entity': /&#?[\da-z]{1,8};/i
    };

    // XQuery language definition
    Prism.languages.xquery = {
        'comment': /\(:[\s\S]*?:\)/,
        'string': {
            pattern: /"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/,
            greedy: true
        },
        'variable': /\$[a-z_][a-z0-9_]*/i,
        'function': /[a-z_][a-z0-9_]*(?=\s*\()/i,
        'keyword': /\b(?:for|let|where|order by|return|if|then|else|some|every|in|satisfies|and|or|not|to|at|as|is|treat|cast|castable|instance of|typeswitch|case|default|switch|typeswitch|empty|sequence|item|node|document|element|attribute|text|comment|processing-instruction|namespace|if|then|else|switch|case|default|typeswitch|try|catch|throw|validate|import|module|declare|variable|function|option|import|schema|import|module|declare|boundary-space|default-collation|base-uri|construction|ordering|empty-order|copy-namespaces|preserve|no-preserve|inherit|no-inherit|xmlspace|strip|preserve|revalidation|skip|strict|lax|type|item|atomic|document|element|attribute|text|comment|processing-instruction|namespace|if|then|else|switch|case|default|typeswitch|try|catch|throw|validate|import|module|declare|variable|function|option|import|schema|import|module|declare|boundary-space|default-collation|base-uri|construction|ordering|empty-order|copy-namespaces|preserve|no-preserve|inherit|no-inherit|xmlspace|strip|preserve|revalidation|skip|strict|lax|type|item|atomic)\b/i,
        'boolean': /\b(?:true|false)\b/i,
        'number': /\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b/i,
        'operator': /[+\-*/=<>!?&|]+/,
        'punctuation': /[()[\]{},;.:]/
    };

    // XPath language definition
    Prism.languages.xpath = {
        'comment': /\(\*[\s\S]*?\*\)/,
        'string': {
            pattern: /"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/,
            greedy: true
        },
        'function': /[a-z_][a-z0-9_]*(?=\s*\()/i,
        'axis': {
            pattern: /(^|[^a-z])(?:ancestor|ancestor-or-self|attribute|child|descendant|descendant-or-self|following|following-sibling|namespace|parent|preceding|preceding-sibling|self)(?![a-z])/i,
            lookbehind: true
        },
        'keyword': /\b(?:and|or|not|mod|div|eq|ne|lt|le|gt|ge|is|as|treat|cast|castable|instance of|if|then|else|for|let|where|order by|return|some|every|in|satisfies|to|at|as|is|treat|cast|castable|instance of|typeswitch|case|default|switch|typeswitch|empty|sequence|item|node|document|element|attribute|text|comment|processing-instruction|namespace)\b/i,
        'boolean': /\b(?:true|false)\b/i,
        'number': /\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b/i,
        'operator': /[+\-*/=<>!?&|]+/,
        'punctuation': /[()[\]{},;.:]|::|@/
    };

    // JSON language definition
    Prism.languages.json = {
        'property': {
            pattern: /"(?:\\.|[^\\"\r\n])*"(?=\s*:)/,
            greedy: true
        },
        'string': {
            pattern: /"(?:\\.|[^\\"\r\n])*"(?!\s*:)/,
            greedy: true
        },
        'comment': /\/\/.*|\/\*[\s\S]*?(?:\*\/|$)/,
        'number': /-?\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b/i,
        'punctuation': /[{}[\],]/,
        'operator': /:/,
        'boolean': /\b(?:true|false)\b/,
        'null': {
            pattern: /\bnull\b/,
            alias: 'keyword'
        }
    };

    // Bash language definition
    Prism.languages.bash = {
        'comment': {
            pattern: /(^|[^"\\])#.*/,
            lookbehind: true
        },
        'string': {
            pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
            greedy: true
        },
        'function': /\b[a-zA-Z_][a-zA-Z0-9_]*\s*\(/,
        'keyword': /\b(?:if|then|else|elif|fi|case|esac|for|select|while|until|do|done|in|function|time|coproc|[|&]|&&|\|\|)\b/,
        'boolean': /\b(?:true|false)\b/,
        'number': /\b\d+(?:\.\d+)?\b/,
        'operator': /[=+\-*/%<>!&|^~]/,
        'punctuation': /[()[\]{};:,]/
    };

    // CSS language definition
    Prism.languages.css = {
        'comment': /\/\*[\s\S]*?\*\//,
        'atrule': {
            pattern: /@[\w-]+(?:[\s\S]*?)?(?:;|$)/,
            inside: {
                'rule': /@[\w-]+/,
                'selector': /[^{}]+/,
                'property': /[^{}]+/
            }
        },
        'url': {
            pattern: /url\((?:(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1|[^)]*)\)/i,
            inside: {
                'function': /^url/i,
                'punctuation': /^\(|\)$/
            }
        },
        'selector': /[^{}\s][^{}]*(?=\s*\{)/,
        'string': {
            pattern: /"(?:\\.|[^"\\\r\n])*"|'(?:\\.|[^'\\\r\n])*'/,
            greedy: true
        },
        'property': /[-_a-z\xA0-\uFFFF][-\w\xA0-\uFFFF]*(?=\s*:)/i,
        'important': /!important\b/i,
        'function': /[-a-z0-9]+(?=\()/i,
        'punctuation': /[(){};:,]/
    };

    // JavaScript language definition
    Prism.languages.javascript = Prism.languages.js = {
        'comment': [
            {
                pattern: /(^|[^\\])\/\*[\s\S]*?(?:\*\/|$)/,
                lookbehind: true
            },
            {
                pattern: /(^|[^\\:])\/\/.*/,
                lookbehind: true,
                greedy: true
            }
        ],
        'string': {
            pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
            greedy: true
        },
        'regex': {
            pattern: /((?:^|[^$\w\xA0-\uFFFF."'\])\s])\s*)\/(?:\[(?:[^\]\\\r\n]|\\.)*\]|\\.|[^/\\\[\r\n])+\/[gimuy]*(?=\s*($|[\r\n,.;})\]]))/,
            lookbehind: true,
            greedy: true
        },
        'template-string': {
            pattern: /`(?:\\[\s\S]|\${(?:[^{}]|{(?:[^{}]|{[^}]*})*})*}|(?!\${)[^\\`])*`/,
            greedy: true,
            inside: {
                'template-punctuation': {
                    pattern: /^`|`$/,
                    alias: 'string'
                },
                'interpolation': {
                    pattern: /((?:^|[^\\])(?:\\{2})*)\${(?:[^{}]|{(?:[^{}]|{[^}]*})*})*}/,
                    lookbehind: true,
                    inside: {
                        'interpolation-punctuation': {
                            pattern: /^\${|}$/,
                            alias: 'punctuation'
                        },
                        'rest': Prism.languages.javascript
                    }
                },
                'string': /[\s\S]+/
            }
        },
        'function': {
            pattern: /(^|[^$\w\xA0-\uFFFF])[a-z\xA0-\uFFFF][$\w\xA0-\uFFFF]*(?=\s*\()/i,
            lookbehind: true
        },
        'keyword': /\b(?:as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)\b/,
        'boolean': /\b(?:true|false)\b/,
        'number': /\b(?:\d+(?:\.\d+)?(?:e[+-]?\d+)?|0x[0-9a-f]+|0b[01]+|0o[0-7]+)\b/i,
        'operator': /--?|\+\+?|!=?=?|<=?|>=?|==?=?|&&?|\|\|?|\?|\*|\/|~|\^|%|&|\||<<|>>|>>>?/,
        'punctuation': /[{}[\];(),.:]/
    };

    // Copy to clipboard functionality
    function addCopyButtons() {
        const codeBlocks = document.querySelectorAll('pre[class*="language-"]');

        codeBlocks.forEach(block => {
            if (block.querySelector('.code-copy-button')) {
                return; // Already has copy button
            }

            const wrapper = document.createElement('div');
            wrapper.style.position = 'relative';
            wrapper.style.display = 'inline-block';
            wrapper.style.width = '100%';

            const copyButton = document.createElement('button');
            copyButton.className = 'code-copy-button';
            copyButton.innerHTML = '<i class="fas fa-copy"></i>';
            copyButton.title = 'Copy to clipboard';

            copyButton.addEventListener('click', () => {
                const text = block.textContent;
                navigator.clipboard.writeText(text).then(() => {
                    copyButton.innerHTML = '<i class="fas fa-check"></i>';
                    copyButton.title = 'Copied!';
                    setTimeout(() => {
                        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                        copyButton.title = 'Copy to clipboard';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                    copyButton.innerHTML = '<i class="fas fa-times"></i>';
                    copyButton.title = 'Copy failed';
                    setTimeout(() => {
                        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                        copyButton.title = 'Copy to clipboard';
                    }, 2000);
                });
            });

            block.parentNode.insertBefore(wrapper, block);
            wrapper.appendChild(block);
            wrapper.appendChild(copyButton);
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addCopyButtons);
    } else {
        addCopyButtons();
    }

    // Export for global use
    window.Prism = Prism;
    window.addCopyButtons = addCopyButtons;

})(typeof Prism !== 'undefined' ? Prism : {});





































