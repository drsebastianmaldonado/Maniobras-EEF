// Animaciones de maniobras: esquema del circuito + trazado intracavitario, sincronizados con un mismo reloj.
// Cada animación tiene dos paneles (una alternativa contra la otra). Los tiempos son ilustrativos.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const CSSA = ['fill', 'stroke', 'fill-opacity'];
  const mk = (t, a, p) => { const e = document.createElementNS(NS, t); for (const k in a) { if (CSSA.includes(k) && String(a[k]).includes('var(')) e.style.setProperty(k, a[k]); else e.setAttribute(k, a[k]); } if (p) p.appendChild(e); return e; };
  const setc = (e, k, v) => e.style.setProperty(k, v);

  // Corazón de los esquemas de la app (OAI ~30°, herramientas/esquemas/corazon.py), con el sistema de conducción.
  const HEART = "<defs>\n<radialGradient id=\"gat\" cx=\"45%\" cy=\"35%\" r=\"75%\"><stop offset=\"0\" stop-color=\"#f7d4cb\"/><stop offset=\".6\" stop-color=\"#e6a091\"/><stop offset=\"1\" stop-color=\"#c97a6b\"/></radialGradient>\n<radialGradient id=\"gvd\" cx=\"40%\" cy=\"38%\" r=\"80%\"><stop offset=\"0\" stop-color=\"#f0b6a8\"/><stop offset=\".65\" stop-color=\"#d27c6c\"/><stop offset=\"1\" stop-color=\"#a9554a\"/></radialGradient>\n<radialGradient id=\"gvi\" cx=\"45%\" cy=\"40%\" r=\"80%\"><stop offset=\"0\" stop-color=\"#eaa696\"/><stop offset=\".65\" stop-color=\"#c86a59\"/><stop offset=\"1\" stop-color=\"#9a4337\"/></radialGradient>\n<radialGradient id=\"gnode\" cx=\"40%\" cy=\"40%\" r=\"70%\"><stop offset=\"0\" stop-color=\"#fff2b0\"/><stop offset=\"1\" stop-color=\"#e3b11c\"/></radialGradient>\n<linearGradient id=\"gcs\" x1=\"0\" x2=\"0\" y1=\"0\" y2=\"1\"><stop offset=\"0\" stop-color=\"#f7d354\"/><stop offset=\"1\" stop-color=\"#e2a915\"/></linearGradient>\n<clipPath id=\"cv\"><path d=\"M96,300 C84,380 104,474 168,550 C206,594 246,616 278,624 L284,300 Z\"/><path d=\"M302,300 C314,420 314,530 304,628 C385,632 464,588 508,508 C546,440 554,350 530,302 Z\"/></clipPath>\n<marker id=\"ab\" viewBox=\"0 0 10 10\" refX=\"8\" refY=\"5\" markerWidth=\"4.5\" markerHeight=\"4.5\" orient=\"auto-start-reverse\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"#1f5fbf\"/></marker>\n<marker id=\"ao\" viewBox=\"0 0 10 10\" refX=\"8\" refY=\"5\" markerWidth=\"4.5\" markerHeight=\"4.5\" orient=\"auto-start-reverse\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"#ef6c00\"/></marker>\n<filter id=\"sh\" x=\"-10%\" y=\"-10%\" width=\"120%\" height=\"120%\"><feDropShadow dx=\"0\" dy=\"3\" stdDeviation=\"4\" flood-color=\"#5d1f16\" flood-opacity=\".25\"/></filter>\n</defs><path d=\"M60,200 C55,110 120,60 190,62 C250,64 285,110 288,170 C290,215 286,250 280,276 L78,282 C66,262 61,236 60,200 Z\" fill=\"url(#gat)\" stroke=\"#9c4f42\" stroke-width=\"2.2\"/>\n<path d=\"M302,276 C296,240 296,200 304,160 C318,100 370,70 430,70 C500,70 548,118 546,190 C545,232 538,262 528,280 Z\" fill=\"url(#gat)\" stroke=\"#9c4f42\" stroke-width=\"2.2\"/>\n<ellipse cx=\"150\" cy=\"130\" rx=\"55\" ry=\"30\" fill=\"#fff\" opacity=\".18\"/><ellipse cx=\"420\" cy=\"128\" rx=\"60\" ry=\"28\" fill=\"#fff\" opacity=\".16\"/>\n<path d=\"M70,284 C170,300 400,302 532,282\" stroke=\"#e9d3a8\" stroke-width=\"18\" fill=\"none\" stroke-linecap=\"round\" opacity=\".85\"/>\n<path d=\"M70,284 C170,300 400,302 532,282\" stroke=\"#c9ad7d\" stroke-width=\"1.2\" fill=\"none\" opacity=\".8\"/>\n<path d=\"M84,292 C70,380 92,480 160,560 C200,605 245,628 284,636 C292,520 292,400 282,300 Z\" fill=\"url(#gvd)\" stroke=\"#9c4f42\" stroke-width=\"2.2\"/>\n<path d=\"M300,300 C312,420 312,530 302,638 C385,642 470,595 516,512 C556,440 566,350 540,294 Z\" fill=\"url(#gvi)\" stroke=\"#9c4f42\" stroke-width=\"2.2\"/>\n<path d=\"M282,300 C292,420 294,530 286,636 L302,638 C312,530 312,420 300,300 Z\" fill=\"#a9564a\" opacity=\".5\"/>\n<ellipse cx=\"170\" cy=\"420\" rx=\"45\" ry=\"80\" fill=\"#fff\" opacity=\".12\"/><ellipse cx=\"430\" cy=\"420\" rx=\"50\" ry=\"90\" fill=\"#fff\" opacity=\".10\"/>\n<text x=\"150\" y=\"185\" font-size=\"16\" font-weight=\"700\" fill=\"#5d1f16\" opacity=\".85\">AD</text>\n<text x=\"440\" y=\"185\" font-size=\"16\" font-weight=\"700\" fill=\"#5d1f16\" opacity=\".85\">AI</text>\n<text x=\"150\" y=\"430\" font-size=\"16\" font-weight=\"700\" fill=\"#5d1f16\" opacity=\".85\">VD</text>\n<text x=\"450\" y=\"430\" font-size=\"16\" font-weight=\"700\" fill=\"#5d1f16\" opacity=\".85\">VI</text>\n<text x=\"294\" y=\"662\" font-size=\"11\" text-anchor=\"middle\" fill=\"#7a4a40\">septum</text>\n<g opacity=\".95\" clip-path=\"url(#cv)\"><path d=\"M172.0,508.0 Q168.8,517.8 169.7,533.9\" stroke=\"url(#gcs)\" stroke-width=\"1.70\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M169.7,533.9 Q169.4,540.7 176.0,549.0\" stroke=\"url(#gcs)\" stroke-width=\"1.16\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M176.0,549.0 Q182.1,551.3 184.0,558.1\" stroke=\"url(#gcs)\" stroke-width=\"0.79\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M184.0,558.1 Q185.0,556.6 191.2,561.3\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M184.0,558.1 Q183.3,562.9 185.7,565.6\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M176.0,549.0 Q175.8,552.3 175.6,560.7\" stroke=\"url(#gcs)\" stroke-width=\"0.79\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M175.6,560.7 Q180.5,567.0 178.5,567.4\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M175.6,560.7 Q173.3,563.8 170.9,568.3\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M169.7,533.9 Q161.8,541.5 161.1,547.1\" stroke=\"url(#gcs)\" stroke-width=\"1.16\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M161.1,547.1 Q160.5,551.3 160.3,558.1\" stroke=\"url(#gcs)\" stroke-width=\"0.79\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M160.3,558.1 Q160.5,559.1 162.0,564.9\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M160.3,558.1 Q162.0,558.4 157.3,565.2\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M161.1,547.1 Q154.4,550.0 152.9,553.6\" stroke=\"url(#gcs)\" stroke-width=\"0.79\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M152.9,553.6 Q154.9,560.8 150.5,560.8\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M152.9,553.6 Q148.3,557.6 145.2,554.6\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M172.0,508.0 Q167.1,492.9 163.1,483.6\" stroke=\"url(#gcs)\" stroke-width=\"1.70\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M163.1,483.6 Q154.3,472.9 148.2,470.1\" stroke=\"url(#gcs)\" stroke-width=\"1.16\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M148.2,470.1 Q144.2,468.0 135.7,468.2\" stroke=\"url(#gcs)\" stroke-width=\"0.79\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M135.7,468.2 Q135.9,469.0 128.4,471.0\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M135.7,468.2 Q128.7,465.9 129.1,463.7\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M148.2,470.1 Q149.8,463.5 143.5,457.4\" stroke=\"url(#gcs)\" stroke-width=\"0.79\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M143.5,457.4 Q136.3,453.8 136.5,451.5\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M143.5,457.4 Q141.1,450.7 142.7,448.7\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M163.1,483.6 Q168.7,473.8 166.4,465.6\" stroke=\"url(#gcs)\" stroke-width=\"1.16\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M166.4,465.6 Q167.7,461.1 164.4,452.7\" stroke=\"url(#gcs)\" stroke-width=\"0.79\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M164.4,452.7 Q159.8,452.3 159.8,446.0\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M164.4,452.7 Q168.5,448.5 167.5,443.8\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M166.4,465.6 Q173.8,465.1 173.7,457.2\" stroke=\"url(#gcs)\" stroke-width=\"0.79\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M173.7,457.2 Q178.0,451.0 175.8,450.7\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M173.7,457.2 Q179.3,459.0 180.9,454.0\" stroke=\"url(#gcs)\" stroke-width=\"0.53\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M238.0,500.0 Q238.4,511.7 232.8,529.5\" stroke=\"url(#gcs)\" stroke-width=\"1.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M232.8,529.5 Q237.8,540.9 236.8,551.4\" stroke=\"url(#gcs)\" stroke-width=\"1.09\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M236.8,551.4 Q241.7,556.2 243.8,563.7\" stroke=\"url(#gcs)\" stroke-width=\"0.74\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M243.8,563.7 Q247.5,567.3 251.7,570.6\" stroke=\"url(#gcs)\" stroke-width=\"0.50\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M243.8,563.7 Q241.0,567.6 243.9,573.7\" stroke=\"url(#gcs)\" stroke-width=\"0.50\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M236.8,551.4 Q235.0,557.0 232.6,564.4\" stroke=\"url(#gcs)\" stroke-width=\"0.74\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M232.6,564.4 Q230.7,568.8 233.0,573.4\" stroke=\"url(#gcs)\" stroke-width=\"0.50\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M232.6,564.4 Q228.6,570.5 225.6,570.8\" stroke=\"url(#gcs)\" stroke-width=\"0.50\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M232.8,529.5 Q226.6,541.7 221.7,549.1\" stroke=\"url(#gcs)\" stroke-width=\"1.09\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M221.7,549.1 Q219.4,554.9 222.3,566.2\" stroke=\"url(#gcs)\" stroke-width=\"0.74\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M222.3,566.2 Q225.3,574.4 227.6,576.1\" stroke=\"url(#gcs)\" stroke-width=\"0.50\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M222.3,566.2 Q220.0,568.6 217.9,577.8\" stroke=\"url(#gcs)\" stroke-width=\"0.50\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M221.7,549.1 Q216.1,553.9 207.7,557.0\" stroke=\"url(#gcs)\" stroke-width=\"0.74\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M207.7,557.0 Q204.2,565.5 201.2,567.4\" stroke=\"url(#gcs)\" stroke-width=\"0.50\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M207.7,557.0 Q204.9,556.5 197.7,558.2\" stroke=\"url(#gcs)\" stroke-width=\"0.50\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M430.0,410.0 Q450.2,404.3 465.5,403.7\" stroke=\"url(#gcs)\" stroke-width=\"1.90\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M465.5,403.7 Q476.6,396.8 486.5,392.2\" stroke=\"url(#gcs)\" stroke-width=\"1.29\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M486.5,392.2 Q490.2,389.8 495.5,380.4\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M495.5,380.4 Q494.7,373.5 496.6,369.8\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M495.5,380.4 Q504.1,375.4 505.5,375.8\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M486.5,392.2 Q492.7,393.1 505.1,391.7\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M505.1,391.7 Q512.2,391.5 517.5,386.1\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M505.1,391.7 Q509.5,392.7 517.0,398.1\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M465.5,403.7 Q479.9,404.4 489.2,408.4\" stroke=\"url(#gcs)\" stroke-width=\"1.29\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M489.2,408.4 Q493.7,406.8 503.2,404.4\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M503.2,404.4 Q506.2,404.8 511.3,398.0\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M503.2,404.4 Q509.4,404.4 514.0,407.3\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M489.2,408.4 Q493.1,412.2 502.7,420.2\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M502.7,420.2 Q506.8,423.9 516.2,422.9\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M502.7,420.2 Q502.0,421.5 507.6,430.3\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M430.0,410.0 Q433.8,428.2 440.9,440.1\" stroke=\"url(#gcs)\" stroke-width=\"1.90\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M440.9,440.1 Q450.1,452.3 456.7,457.4\" stroke=\"url(#gcs)\" stroke-width=\"1.29\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M456.7,457.4 Q464.7,463.0 471.7,465.5\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M471.7,465.5 Q477.7,463.4 483.6,466.9\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M471.7,465.5 Q473.8,471.6 477.6,474.8\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M456.7,457.4 Q457.0,468.9 464.9,473.1\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M464.9,473.1 Q472.5,478.6 474.5,478.8\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M464.9,473.1 Q470.0,481.3 467.2,486.2\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M440.9,440.1 Q436.1,452.2 437.5,462.4\" stroke=\"url(#gcs)\" stroke-width=\"1.29\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M437.5,462.4 Q440.0,472.9 440.1,477.0\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M440.1,477.0 Q443.7,478.7 445.2,484.4\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M440.1,477.0 Q441.5,484.8 437.6,486.4\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M437.5,462.4 Q437.1,467.8 428.9,475.5\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M428.9,475.5 Q428.9,481.6 428.8,486.9\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M428.9,475.5 Q425.2,475.3 418.4,481.3\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M400.0,520.0 Q417.5,529.5 429.4,537.0\" stroke=\"url(#gcs)\" stroke-width=\"1.90\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M429.4,537.0 Q441.5,534.4 449.8,539.3\" stroke=\"url(#gcs)\" stroke-width=\"1.29\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M449.8,539.3 Q454.8,540.2 461.9,534.9\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M461.9,534.9 Q463.9,530.8 469.1,528.6\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M461.9,534.9 Q465.1,537.1 471.5,536.2\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M449.8,539.3 Q460.6,540.3 464.4,544.8\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M464.4,544.8 Q470.6,547.5 474.9,544.7\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M464.4,544.8 Q466.8,551.1 472.6,550.7\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M429.4,537.0 Q434.3,548.2 443.7,552.4\" stroke=\"url(#gcs)\" stroke-width=\"1.29\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M443.7,552.4 Q451.0,552.6 458.2,558.9\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M458.2,558.9 Q467.6,555.9 469.1,558.1\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M458.2,558.9 Q463.6,566.1 466.3,566.7\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M443.7,552.4 Q444.8,556.9 451.0,566.0\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M451.0,566.0 Q454.1,572.3 459.9,570.8\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M451.0,566.0 Q455.6,573.4 453.0,577.8\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M400.0,520.0 Q396.2,536.8 389.7,548.2\" stroke=\"url(#gcs)\" stroke-width=\"1.90\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M389.7,548.2 Q388.9,557.3 393.9,566.8\" stroke=\"url(#gcs)\" stroke-width=\"1.29\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M393.9,566.8 Q396.9,574.0 402.0,577.4\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M402.0,577.4 Q402.4,577.2 410.3,582.6\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M402.0,577.4 Q401.9,583.3 403.9,586.0\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M393.9,566.8 Q390.9,575.2 392.8,578.3\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M392.8,578.3 Q394.0,578.9 395.3,586.8\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M392.8,578.3 Q389.9,581.4 389.3,585.4\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M389.7,548.2 Q381.9,555.6 377.4,562.1\" stroke=\"url(#gcs)\" stroke-width=\"1.29\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M377.4,562.1 Q378.7,568.3 372.5,573.9\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M372.5,573.9 Q374.0,579.2 373.9,582.9\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M372.5,573.9 Q367.5,575.2 367.6,580.0\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M377.4,562.1 Q371.8,569.0 365.6,568.5\" stroke=\"url(#gcs)\" stroke-width=\"0.88\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M365.6,568.5 Q361.2,571.9 359.6,574.8\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/><path d=\"M365.6,568.5 Q364.5,569.7 357.2,569.3\" stroke=\"url(#gcs)\" stroke-width=\"0.60\" fill=\"none\" stroke-linecap=\"round\"/></g>\n<path d=\"M250,262 C255,250 275,248 284,258 C288,266 280,274 268,273 C258,272 248,270 250,262 Z\" fill=\"url(#gnode)\" stroke=\"#9a7300\" stroke-width=\"1.5\"/>\n<path d=\"M282.0,270.0 L282.7,271.5 L283.5,273.0 L284.2,274.4 L284.8,275.9 L285.5,277.3 L286.1,278.8 L286.7,280.2 L287.3,281.6 L287.9,283.1 L288.4,284.5 L288.9,286.0 L289.4,287.5 L289.8,289.0 L290.3,290.5 L290.7,292.1 L291.0,293.7 L291.4,295.3 L291.7,297.0 L292.0,298.7 L292.3,300.5 L292.5,302.3 L292.7,304.1 L292.9,306.0 L293.0,308.0\" stroke=\"url(#gcs)\" stroke-width=\"7\" fill=\"none\" stroke-linecap=\"round\"/>\n<path d=\"M290.0,308.0 L289.2,317.0 L288.3,325.9 L287.4,334.9 L286.3,343.8 L285.1,352.6 L283.8,361.3 L282.5,370.0 L281.0,378.7 L279.3,387.2 L277.6,395.7 L275.7,404.0 L273.8,412.2 L271.6,420.4 L269.3,428.4 L266.9,436.3 L264.4,444.0 L261.7,451.6 L258.8,459.0 L255.7,466.3 L252.5,473.4 L249.2,480.3 L245.6,487.1 L241.9,493.6 L238.0,500.0\" stroke=\"url(#gcs)\" stroke-width=\"3\" fill=\"none\" stroke-linecap=\"round\"/>\n<path d=\"M238.0,500.0 L235.7,501.5 L233.4,502.9 L230.9,504.2 L228.5,505.5 L225.9,506.6 L223.3,507.7 L220.7,508.7 L218.0,509.6 L215.3,510.4 L212.5,511.2 L209.7,511.8 L206.9,512.2 L204.0,512.6 L201.1,512.9 L198.2,513.0 L195.3,513.0 L192.4,512.9 L189.5,512.7 L186.6,512.3 L183.6,511.7 L180.7,511.0 L177.8,510.2 L174.9,509.2 L172.0,508.0\" stroke=\"url(#gcs)\" stroke-width=\"3.4\" fill=\"none\" stroke-linecap=\"round\"/>\n<path d=\"M295.0,308.0 L295.6,309.2 L296.3,310.5 L296.9,311.7 L297.6,312.8 L298.2,314.0 L298.9,315.2 L299.6,316.3 L300.3,317.4 L301.0,318.5 L301.7,319.6 L302.4,320.7 L303.1,321.8 L303.8,322.8 L304.6,323.9 L305.3,324.9 L306.0,325.9 L306.8,327.0 L307.5,328.0 L308.3,329.0 L309.0,330.0 L309.8,331.0 L310.5,332.0 L311.3,333.0 L312.0,334.0\" stroke=\"url(#gcs)\" stroke-width=\"5\" fill=\"none\" stroke-linecap=\"round\"/>\n<path d=\"M312.0,334.0 L316.8,336.1 L321.7,338.3 L326.8,340.6 L331.9,343.1 L337.0,345.7 L342.2,348.4 L347.5,351.2 L352.8,354.1 L358.1,357.2 L363.4,360.3 L368.7,363.5 L374.0,366.8 L379.2,370.1 L384.4,373.5 L389.5,377.0 L394.5,380.5 L399.4,384.1 L404.2,387.7 L408.9,391.4 L413.5,395.1 L417.9,398.8 L422.1,402.5 L426.1,406.3 L430.0,410.0\" stroke=\"url(#gcs)\" stroke-width=\"3.2\" fill=\"none\" stroke-linecap=\"round\"/>\n<path d=\"M312.0,334.0 L314.3,342.3 L316.7,350.6 L319.3,358.9 L322.0,367.2 L324.8,375.6 L327.7,383.9 L330.8,392.2 L333.9,400.4 L337.2,408.7 L340.6,416.8 L344.1,425.0 L347.8,433.0 L351.5,441.0 L355.4,448.8 L359.3,456.6 L363.4,464.2 L367.6,471.7 L371.9,479.1 L376.3,486.4 L380.8,493.4 L385.5,500.4 L390.2,507.1 L395.1,513.6 L400.0,520.0\" stroke=\"url(#gcs)\" stroke-width=\"3.2\" fill=\"none\" stroke-linecap=\"round\"/>\n<text x=\"210\" y=\"252\" font-size=\"10.5\" text-anchor=\"end\" fill=\"#6d4c41\">nodo AV</text>\n<text x=\"274\" y=\"320\" font-size=\"10.5\" text-anchor=\"end\" fill=\"#6d4c41\">His</text>";
  const ATR = ['M60,200 C55,110 120,60 190,62 C250,64 285,110 288,170 C290,215 286,250 280,276 L78,282 C66,262 61,236 60,200 Z',
               'M302,276 C296,240 296,200 304,160 C318,100 370,70 430,70 C500,70 548,118 546,190 C545,232 538,262 528,280 Z'];
  const VEN = ['M84,292 C70,380 92,480 160,560 C200,605 245,628 284,636 C292,520 292,400 282,300 Z',
               'M300,300 C312,420 312,530 302,638 C385,642 470,595 516,512 C556,440 566,350 540,294 Z'];
  // Puntos del recorrido (coordenadas del corazón)
  const G = { aSep: [232, 238], node: [268, 262], his: [293, 308], rb1: [288, 380], rb2: [270, 450], rb3: [238, 500], rb4: [200, 545], apex: [180, 562],
              lvA: [430, 410], lvB: [505, 345], apV: [526, 306], apA: [527, 262], la: [470, 200], focus: [140, 140], ra: [170, 180], base: [250, 345], ph: [278, 300], hra: [140, 108], cso: [215, 290], jx: [287, 288], ralat: [92, 238], afA: [92, 272], afV: [178, 512], vtf: [150, 470], sn: [196, 82], cs: [516, 290] };
  const VB = '15 50 560 625';
  // Desde el His el frente baja por las dos ramas: la derecha hasta el ápex del VD y la izquierda hasta la pared lateral del VI
  const ramas = (h, HV) => [
    { c: 'ante', pts: [[G.his, h], [G.rb1, h + 12], [G.rb2, h + 22], [G.rb3, h + 30], [G.rb4, h + 38], [G.apex, h + HV]] },
    { c: 'ante', pts: [[G.his, h], [[312, 334], h + 8], [[360, 365], h + 20], [[405, 392], h + 32], [G.lvA, h + HV]] }];

  // ---------- Escenarios ----------
  // Cada uno devuelve { ev: eventos del trazado, wv: frentes que se mueven, flA / flV: activaciones para iluminar cámaras, ... }
  function travVop() {
    const LC = 340, VA = 110, AH = 185, HV = 45, SC = 300, ev = [], wv = [], flA = [], flV = [];
    const ante = (a, ah, stop) => { const h = a + ah; ev.push({ ch: 'His', t: h, l: 'H' });
      const pts = [[G.aSep, a], [G.node, a + 30], [G.his, h]];
      wv.push({ c: 'ante', pts }); if (!stop) wv.push(...ramas(h, HV)); if (!stop) { ev.push({ ch: 'VD', t: h + HV, l: 'V' }); flV.push(h + HV); } return h + HV; };
    // retrógrada por la vía: desde el VI (activado por el sistema de conducción) o desde el catéter del VD (estimulado)
    const retro = (v, sa, paced) => { const a = v + sa;
      const pts = paced ? [[G.apex, v], [[260, 600], v + 30], [[400, 560], v + 70], [[500, 430], v + 110], [G.apV, v + sa - 15], [G.apA, a], [G.la, a + 30]]
                        : [[G.lvA, v], [G.lvB, v + 40], [G.apV, v + sa - 15], [G.apA, a], [G.la, a + 30]];
      wv.push({ c: 'retro', pts }); ev.push({ ch: 'AD', t: a, l: 'A' }); flA.push(a); return a; };
    // taquicardia
    let a = 170; ev.push({ ch: 'VD', t: 60, l: 'V' }); flV.push(60); wv.push({ c: 'retro', pts: [[G.lvA, 60], [G.lvB, 100], [G.apV, 155], [G.apA, a], [G.la, a + 30]] }); ev.push({ ch: 'AD', t: a, l: 'A' }); flA.push(a);
    let v = ante(a, AH); a = retro(v, VA);
    ante(a, AH, true);                             // la A siguiente baja hasta el His y choca con la estimulación
    const S = [700, 1000, 1300, 1600, 1900];
    S.forEach((s, i) => {
      ev.push({ ch: 'VD', t: s, l: 'E', stim: true }); flV.push(s);
      a = retro(s, 150, true);
      if (i < S.length - 1) ante(a, AH + 5, true);
    });
    const lastA = a;
    ev.find(e => e.t === lastA && e.ch === 'AD').tag = 'última A acelerada';
    v = ante(lastA, AH + 10);                     // el último A conduce al V: A-V
    for (let k = 0; k < 5; k++) { a = retro(v, VA); v = ante(a, AH); }   // la taquicardia retoma su ciclo
    return { title: 'TRAV (o TRNAV): respuesta A-V', ap: true, ev, wv, flA, flV, stimEnd: 1900, verdictT: lastA + AH + 10 + HV,
      verdict: 'Después de la última A acelerada viene un V: <b>A-V</b>. Excluye la TA.',
      why: 'La A estimulada viajó por el circuito (V → vía → A) y sigue bajando por el nodo: la taquicardia continúa con el V.' };
  }

  function taVop() {
    const LC = 340, AH = 120, HV = 45, ev = [], wv = [], flA = [], flV = [];
    const focusBeat = (a, stop) => {
      ev.push({ ch: 'AD', t: a, l: 'A' }); flA.push(a);
      wv.push({ c: 'focus', pts: [[G.focus, a], [[195, 195], a + 20], [G.aSep, a + 35]] });
      const h = a + AH; ev.push({ ch: 'His', t: h, l: 'H' });
      const pts = [[G.aSep, a + 35], [G.node, a + 60], [G.his, h]];
      wv.push({ c: 'ante', pts }); if (!stop) wv.push(...ramas(h, HV));
      if (!stop) { ev.push({ ch: 'VD', t: h + HV, l: 'V' }); flV.push(h + HV); }
    };
    focusBeat(60); focusBeat(400); focusBeat(740, true);
    const S = [860, 1160, 1460, 1760, 2060];
    let lastA = 0;
    S.forEach(s => {
      ev.push({ ch: 'VD', t: s, l: 'E', stim: true }); flV.push(s);
      const h = s + 60, a = s + 160;
      ev.push({ ch: 'His', t: h, l: 'H' }); ev.push({ ch: 'AD', t: a, l: 'A' }); flA.push(a);
      wv.push({ c: 'retro', pts: [[G.apex, s], [G.rb4, s + 15], [G.rb3, s + 28], [G.rb2, s + 38], [G.rb1, s + 48], [G.his, h], [G.node, a - 30], [G.aSep, a], [G.ra, a + 25]] });
      lastA = a;
    });
    ev.find(e => e.t === lastA && e.ch === 'AD').tag = 'última A acelerada';
    const f1 = lastA + 360;                       // el foco vuelve a disparar: A-A
    for (let k = 0; k < 5; k++) focusBeat(f1 + k * LC);   // el foco retoma su ciclo
    Object.assign(ev.find(e => e.t === f1 && e.ch === 'AD'), { tag: 'otra A (foco)', tagUp: true });
    return { title: 'TA: respuesta A-A-V', focus: true, ev, wv, flA, flV, stimEnd: 2060, verdictT: f1 + AH + HV,
      verdict: 'Después de la última A acelerada viene <b>otra A</b> y recién después el V: <b>A-A-V</b>. Es TA.',
      why: 'La A estimulada subió por el nodo y no puede volver a bajar. La taquicardia sigue porque el foco auricular dispara de nuevo.' };
  }


  // ---------- Motor común para las maniobras de estimulación ventricular durante la TSV ----------
  const LCT = 340, HVT = 45, VBO = 25;            // LC de la TSV, HV, retraso del V basal respecto del apical
  const HR = { apex: 60, base: 105 };              // estímulo → His retrógrado, según el sitio
  const cut = (pts, tc) => { const o = []; for (let i = 0; i < pts.length; i++) { const [p, t] = pts[i]; if (t <= tc) { o.push(pts[i]); continue; }
    if (i > 0) { const [p0, t0] = pts[i - 1], f = (tc - t0) / Math.max(1, t - t0); o.push([[p0[0] + (p[0] - p0[0]) * f, p0[1] + (p[1] - p0[1]) * f], tc]); } break; } return o; };
  const at = (pts, tc) => { const c = cut(pts, tc); return c.length ? c[c.length - 1][0] : pts[0][0]; };
  const newSc = o => Object.assign({ ev: [], wv: [], flA: [], flV: [], ints: [], cols: [], stims: [], notes: [], m: {} }, o);
  const E = (sc, ch, t, l, x) => { const e = Object.assign({ ch, t, l }, x); sc.ev.push(e); if (ch === 'AD') sc.flA.push(t); return e; };
  const W_ = (sc, c, pts, tc) => { const p = tc == null ? pts : cut(pts, tc); if (p.length > 1) sc.wv.push({ c, pts: p }); if (tc != null && tc < pts[pts.length - 1][1]) sc.cols.push({ t: tc, pt: at(pts, tc) }); };
  const Vs = (sc, h) => { E(sc, 'VD', h + HVT, 'V'); E(sc, 'VDb', h + HVT + VBO, 'V'); sc.flV.push(h + HVT); };
  const down = (sc, h, tcR, tcL) => { const [r, l] = ramas(h, HVT); W_(sc, 'ante', r.pts, tcR); W_(sc, 'ante', l.pts, tcL); };
  const stim = (sc, site, s) => { E(sc, site === 'base' ? 'VDb' : 'VD', s, 'E', { stim: true }); sc.flV.push(s); sc.stims.push({ t: s, pt: G[site] }); };
  const rbUp = (site, s) => site === 'base'
    // desde la base el frente baja por el miocardio hasta el Purkinje de la punta y recién ahí sube por toda la rama derecha
    ? [[G.base, s], [[226, 430], s + 30], [[196, 515], s + 55], [G.rb4, s + 60], [G.rb3, s + 73], [G.rb2, s + 83], [G.rb1, s + 93], [G.his, s + 105], [G.node, s + 140]]
    : [[G.apex, s], [G.rb4, s + 15], [G.rb3, s + 28], [G.rb2, s + 38], [G.rb1, s + 48], [G.his, s + 60], [G.node, s + 95]];
  const APS = { sep: [232, 268], sepV: [236, 312] };
  // Vía septal: retrógrada desde el septum (latido conducido) o desde el sitio de estimulación
  const VIA = {
    sep: { dS: { apex: 145, base: 105 }, dAP: 135,
      desc: h => [[[300, 345], h + 20], [[262, 332], h + 60], [APS.sepV, h + 135], [APS.sep, h + 150], [[200, 215], h + 178], [G.ra, h + 198]],
      paced: (site, s) => site === 'base'
        ? [[G.base, s], [[240, 330], s + 50], [APS.sepV, s + 105], [APS.sep, s + 117], [[200, 215], s + 145], [G.ra, s + 165]]
        : [[G.apex, s], [[205, 470], s + 50], [[226, 380], s + 100], [APS.sepV, s + 145], [APS.sep, s + 157], [[200, 215], s + 185], [G.ra, s + 205]] } };

  // TRAV ortodrómica. o: { PCL, AHp (AH de los latidos estimulados), AHr (AH del retorno), runs: [{ site, n }] }
  function simTRAV(o) {
    const sc = newSc({ ap: 'sep', title: o.title }), V = VIA.sep, AH = 185;
    const beat = (a, ah, mk) => { const h = a + ah; E(sc, 'His', h, 'H'); W_(sc, 'ante', [[G.aSep, a], [G.node, a + 30], [G.his, h]]); down(sc, h); Vs(sc, h);
      W_(sc, 'retro', V.desc(h)); const a2 = h + V.dAP + 20; E(sc, 'AD', a2, 'A'); if (mk) mk(h, a2); return a2; };
    let a = 120; E(sc, 'AD', a, 'A');
    const tachy = (k, first) => { const out = []; for (let i = 0; i < k; i++) { const ah = i === 0 && first ? first : AH; const h = a + ah; out.push({ h, v: h + HVT, a0: a }); a = beat(a, ah); out[i].a = a; } return out; };
    sc.m.pre = tachy(2);
    sc.m.runs = [];
    o.runs.forEach((r, ri) => {
      let prev = { a, paced: false }, s = sc.ev.filter(e => e.ch === 'VD' && !e.stim).pop().t + o.PCL; const R = { site: r.site, S: [], H: [], A: [] };
      for (let k = 0; k < r.n; k++, s += o.PCL) {
        stim(sc, r.site, s); R.S.push(s);
        const rH = s + HR[r.site], oh = prev.a + (prev.paced ? o.AHp : AH), rb = rbUp(r.site, s), ante = [[G.aSep, prev.a], [G.node, prev.a + 30], [G.his, oh]];
        if (oh < rH) {                                   // el frente que bajó por el nodo llega primero al His: His ortodrómico
          R.H.push(E(sc, 'His', oh, 'H')); W_(sc, 'ante', ante);
          const tc = (oh + rH) / 2, dAP = oh + V.dAP, pAP = s + V.dS[r.site];
          W_(sc, 'retro', rb, tc);
          if (dAP < pAP) { down(sc, oh, tc); W_(sc, 'retro', V.desc(oh)); W_(sc, 'retro', V.paced(r.site, s), (dAP + pAP) / 2); prev = { a: oh + V.dAP + 20, paced: false }; }
          else { down(sc, oh, tc, oh + 25); W_(sc, 'retro', V.paced(r.site, s)); prev = { a: s + V.dS[r.site] + 15, paced: true }; }
        } else {                                         // el estímulo sube por la rama y activa el His de abajo hacia arriba
          R.H.push(E(sc, 'His', rH, 'H', { inv: true })); const tc = rH + 12;
          W_(sc, 'ante', ante, tc); W_(sc, 'retro', rb, tc); W_(sc, 'retro', V.paced(r.site, s)); prev = { a: s + V.dS[r.site] + 15, paced: true };
        }
        E(sc, 'AD', prev.a, 'A'); R.A.push(prev.a);
      }
      a = prev.a; R.lastS = s - o.PCL; R.lastA = a;
      R.ret = tachy(ri === o.runs.length - 1 ? 5 : 3, o.AHr);
      sc.m.runs.push(R);
    });
    sc.stimEnd = sc.m.runs[sc.m.runs.length - 1].lastS; return sc;
  }

  // TRNAV típica (baja por la vía lenta, sube por la rápida); n = giro en la vía final común inferior
  function simTRNAV(o) {
    const sc = newSc({ nodal: true, title: o.title }), SLOW = 255;
    const slow = a => [[[226, 248], a], [[206, 268], a + 70], [[220, 292], a + 150], [[250, 284], a + 220], [G.node, a + SLOW]];
    const fast = n => { W_(sc, 'retro', [[G.node, n], [[252, 246], n + 30], [[232, 236], n + 55], [[200, 212], n + 75], [G.ra, n + 95]]); E(sc, 'AD', n + 85, 'A'); return n + 85; };
    const turn = (n, full) => { E(sc, 'His', n + 30, 'H'); W_(sc, 'ante', [[G.node, n], [G.his, n + 30]]); if (full) { down(sc, n + 30); Vs(sc, n + 30); } return fast(n); };
    let a = 120; E(sc, 'AD', a, 'A');
    const tachy = (k, dec) => { const out = []; for (let i = 0; i < k; i++) { const n = a + SLOW + (i === 0 ? dec || 0 : 0); W_(sc, 'ante', slow(a).map(([p, t], j, arr) => [p, j === arr.length - 1 ? n : t]));
      a = turn(n, true); out.push({ h: n + 30, v: n + 30 + HVT, a }); } return out; };
    sc.m.pre = tachy(2);
    sc.m.runs = [];
    o.runs.forEach((r, ri) => {
      let prev = { a, dec: 0 }, s = sc.ev.filter(e => e.ch === 'VD' && !e.stim).pop().t + o.PCL; const R = { site: r.site, S: [], H: [], A: [], cap: [] };
      for (let k = 0; k < r.n; k++, s += o.PCL) {
        stim(sc, r.site, s); R.S.push(s);
        const rH = s + HR[r.site], rn = rH + 35, nd = prev.a + SLOW + prev.dec, sl = slow(prev.a).map(([p, t], j, arr) => [p, j === arr.length - 1 ? nd : t]), rb = rbUp(r.site, s);
        if (nd < rn) {                                   // la vía lenta llega antes: el latido de la TSV sigue igual (el V no es parte del circuito)
          W_(sc, 'ante', sl); R.H.push(E(sc, 'His', nd + 30, 'H')); W_(sc, 'ante', [[G.node, nd], [G.his, nd + 30]]);
          const tc = (nd + 30 + rH) / 2; down(sc, nd + 30, tc, tc); W_(sc, 'retro', rb, tc);
          prev = { a: fast(nd), dec: 0 }; R.cap.push(false);
        } else {                                         // el estímulo llega primero al nodo y sube por la vía rápida
          const tc = (nd + rn) / 2; W_(sc, 'ante', sl, tc - 10); R.H.push(E(sc, 'His', rH, 'H', { inv: true })); W_(sc, 'retro', rb);
          prev = { a: fast(rn), dec: 10 }; R.cap.push(true);
        }
        R.A.push(prev.a);
      }
      a = prev.a; R.lastS = s - o.PCL; R.lastA = a;
      R.ret = tachy(ri === o.runs.length - 1 ? 5 : 3, 10);
      sc.m.runs.push(R);
    });
    sc.stimEnd = sc.m.runs[sc.m.runs.length - 1].lastS; return sc;
  }

  const sg = d => (d > 0 ? '+' : d < 0 ? '−' : '') + Math.abs(d);
  const brk = (sc, ch, t0, t1, l, x) => sc.ints.push(Object.assign({ ch, t0, t1, l }, x));
  const ENT = { PCL: 300, AHp: 205, AHr: 195 };
  // PPI − LC, SA − VA y ΔHA: el mismo encarrilamiento desde el ápex del VD, medido de tres maneras
  function entr(kind, mech) {
    const sc = mech === 'trav' ? simTRAV(Object.assign({ title: 'TRAV por vía septal', runs: [{ site: 'apex', n: 7 }] }, ENT))
                               : simTRNAV(Object.assign({ title: 'TRNAV típica', runs: [{ site: 'apex', n: 7 }] }, ENT));
    const [p0, p1] = sc.m.pre, R = sc.m.runs[0], ret = R.ret[0], trav = mech === 'trav', all = kind === 'all';
    const lastH = R.H[R.H.length - 1].t, dx = trav ? 'TRAV' : 'TRNAV', V = [], W = [];
    const lt = (d, c) => `(${d < c ? '&lt;' : '&gt;'} ${c})`;
    if (kind === 'ppi' || all) {
      const ppi = ret.v - R.lastS, d = ppi - LCT;
      brk(sc, 'VD', p0.v, p1.v, 'LC ' + LCT); brk(sc, 'VD', R.lastS, ret.v, 'PPI ' + ppi, { hot: 1 });
      V.push([ret.v, `PPI − LC = ${ppi} − ${LCT} = <b>${d} ms</b> ${lt(d, 115)}` + (all ? '' : `: ${trav ? 'el VD está cerca del circuito' : 'el VD está lejos del circuito'} → <b>${dx}</b>.`)]);
      W.push(trav ? 'El estímulo entra al circuito por el ventrículo, sube por la vía y vuelve por el nodo: el retorno recorre solo el circuito.'
                  : 'El estímulo tiene que subir por la rama derecha y el His hasta el nodo, dar la vuelta al circuito y volver a bajar: el retorno suma ida y vuelta por el His-Purkinje.');
    }
    if (kind === 'sava' || all) {
      const va = p1.a - p1.v, sa = R.lastA - R.lastS, d = sa - va;
      brk(sc, 'AD', p1.v, p1.a, 'VA ' + va, { guide: 'VD' }); brk(sc, 'AD', R.lastS, R.lastA, 'SA ' + sa, { guide: 'VD', hot: 1 });
      V.push([R.lastA, `SA − VA = ${sa} − ${va} = <b>${d} ms</b> ${lt(d, 85)}` + (all ? '' : ` → <b>${dx}</b>.`)]);
      W.push(trav ? 'En la TSV y al estimular, V y A se activan en serie a través de la vía: el SA es apenas más largo que el VA.'
                  : 'En la TSV, V y A se activan en paralelo desde el nodo (VA casi 0); al estimular, en serie (V → His → nodo → A): el SA es mucho más largo.');
    }
    if (kind === 'dha' || all) {
      const hat = p1.a - p1.h, hap = R.lastA - lastH, d = hap - hat, ch = all ? 'His' : 'AD', g = all ? null : 'His';
      brk(sc, ch, p1.h, p1.a, 'HA ' + hat, { guide: g }); brk(sc, ch, lastH, R.lastA, 'HA ' + hap, { guide: g, hot: 1 });
      V.push([R.lastA, (all ? '' : 'ΔHA = HA estimulando − HA en TSV = ') + `${all ? 'ΔHA = ' : ''}${hap} − ${hat} = <b>${sg(d)} ms</b> (${d < 0 ? '&lt; 0' : '&gt; 0'})` + (all ? '' : ` → <b>${dx}</b>.`)]);
      W.push(trav ? 'En la TSV el His y la A se activan en serie (His → V → vía → A); al estimular, en paralelo (la rama sube al His y la vía a la aurícula): el HA se acorta.'
                  : 'En la TSV el His y la A se activan en paralelo desde el nodo (seudointervalo corto); al estimular, en serie (His → nodo → A): el HA se alarga.');
    }
    const vt = Math.max(...V.map(v => v[0]));
    Object.assign(sc, all ? { verdictT: vt, verdict: V.map(v => v[1]).join('<br>') + `<br>Las tres → <b>${dx}</b>.`,
        why: trav ? 'El ventrículo es parte del circuito y la vía conecta V y A en serie.' : 'El ventrículo está fuera del circuito: el estímulo tiene que subir por el His hasta el nodo.' }
      : { verdictT: vt, verdict: V[0][1], why: W[0] });
    return sc;
  }

  // Captura ortodrómica del His: misma TRAV a dos LC de estimulación
  function hisorto(pcl) {
    const ortho = pcl > 300;
    const sc = simTRAV({ title: ortho ? `TRAV, estimulando a ${pcl} ms` : `TRAV, estimulando a ${pcl} ms`, PCL: pcl, AHp: ortho ? 190 : 215, AHr: ortho ? 185 : 200, runs: [{ site: 'apex', n: 7 }] });
    const R = sc.m.runs[0], k = R.H.length - 2, h = R.H[k];
    Object.assign(h, { tag: ortho ? 'H ortodrómico' : 'H retrógrado', tagT: h.t + 1 });
    sc.ortho = ortho;
    if (ortho) brk(sc, 'His', R.A[k - 1], h.t, 'AH ' + (h.t - R.A[k - 1]), { hot: 1 });
    Object.assign(sc, { verdictT: h.t + 20,
      verdict: ortho ? 'El His se activa <b>de arriba hacia abajo</b>, con el mismo AH que en la TSV, aunque el ventrículo esté estimulado: <b>captura ortodrómica del His</b>.' : 'El estímulo sube por la rama derecha y llega primero al His: <b>His retrógrado</b> (morfología distinta de la TSV).',
      why: ortho ? 'El frente bajó por el nodo y chocó con el del estímulo en la rama derecha. La aurícula se activó por otro camino: hay una vía y participa del circuito.'
                 : 'A LC cortas es lo esperable, haya o no vía: es inespecífico.' });
    return sc;
  }

  // Encarrilamiento diferencial: el mismo mecanismo encarrilado desde el ápex y desde la base del VD
  function diffSc(mech) {
    const trav = mech === 'trav', o = Object.assign({ title: trav ? 'TRAV por vía septal' : 'TRNAV típica', runs: [{ site: 'apex', n: 7 }, { site: 'base', n: 7 }] }, ENT);
    const sc = trav ? simTRAV(o) : simTRNAV(o); sc.cats = ['apex', 'base'];
    const [ra, rb] = sc.m.runs, vaA = ra.lastA - ra.lastS, vaB = rb.lastA - rb.lastS, pA = ra.ret[0].v - ra.lastS - LCT, pB = rb.ret[0].v + VBO - rb.lastS - LCT;
    brk(sc, 'AD', ra.lastS, ra.lastA, 'VA ápex ' + vaA, { guide: 'VD', hot: 1 }); brk(sc, 'AD', rb.lastS, rb.lastA, 'VA base ' + vaB, { guide: 'VDb', hot: 1 });
    brk(sc, 'VD', ra.lastS, ra.ret[0].v, 'PPI ' + (pA + LCT), { hot: 1 }); brk(sc, 'VDb', rb.lastS, rb.ret[0].v + VBO, 'PPI ' + (pB + LCT), { hot: 1 });
    const dva = vaB - vaA, dp = pB - pA, nav = dva > 20 || dp > 30;
    Object.assign(sc, { verdictT: rb.ret[0].v + VBO, verdict: `ΔVA (base − ápex) = ${vaB} − ${vaA} = <b>${sg(dva)}</b>; ΔPPI−LC = ${pB} − ${pA} = <b>${sg(dp)}</b> → <b>${nav ? 'TRNAV' : 'TRAV'}</b>.`,
      why: trav ? 'La base está al lado de la vía septal: desde ahí el estímulo llega antes al circuito, así que el VA y el PPI no se alargan (incluso se acortan).'
                : 'El circuito se alcanza por el Purkinje, que se entra cerca del ápex: desde la base el estímulo tiene que bajar hasta el Purkinje y subir. VA y PPI se alargan.' });
    sc.stimEnd = ra.lastS; return sc;
  }


  // ---------- Grupo 2 ----------
  // Latidos sueltos de cada mecanismo, para armar escenarios que no son un encarrilamiento
  const travBeat = (sc, a, ah) => { const h = a + (ah || 185); E(sc, 'His', h, 'H'); W_(sc, 'ante', [[G.aSep, a], [G.node, a + 30], [G.his, h]]); down(sc, h); Vs(sc, h);
    W_(sc, 'retro', VIA.sep.desc(h)); const a2 = h + VIA.sep.dAP + 20; E(sc, 'AD', a2, 'A'); return { h, a: a2 }; };
  const NSLOW = 255;
  const slowP = (a, nd) => [[[226, 248], a], [[206, 268], a + 70], [[220, 292], a + 150], [[250, 284], a + 220], [G.node, nd]];
  const fastUp = (sc, n) => { W_(sc, 'retro', [[G.node, n], [[252, 246], n + 30], [[232, 236], n + 55], [[200, 212], n + 75], [G.ra, n + 95]]); E(sc, 'AD', n + 85, 'A'); return n + 85; };
  const nodeUp = (sc, tn) => { W_(sc, 'retro', [[G.node, tn], [G.aSep, tn + 40], [G.ra, tn + 85]]); E(sc, 'AD', tn + 85, 'A'); return tn + 85; };
  const trnavBeat = (sc, a, cutDown) => { const n = a + NSLOW; W_(sc, 'ante', slowP(a, n)); E(sc, 'His', n + 30, 'H'); W_(sc, 'ante', [[G.node, n], [G.his, n + 30]]);
    if (cutDown) down(sc, n + 30, cutDown, cutDown); else { down(sc, n + 30); Vs(sc, n + 30); } return { n, h: n + 30, a: fastUp(sc, n) }; };

  // EV con His refractario durante la TSV, desde la base del VD
  function ehrSc(mech) {
    const trav = mech === 'trav', sc = newSc({ title: trav ? 'TRAV por vía septal' : 'TRNAV típica', cats: ['base'] });
    if (trav) sc.ap = 'sep'; else sc.nodal = true;
    let a = 120, b; E(sc, 'AD', a, 'A');
    const As = [a];
    for (let i = 0; i < 2; i++) { b = trav ? travBeat(sc, a) : trnavBeat(sc, a); a = b.a; As.push(a); }
    let e, hRef, aNew, aExp;
    if (trav) {
      const h = a + 185; hRef = E(sc, 'His', h, 'H'); W_(sc, 'ante', [[G.aSep, a], [G.node, a + 30], [G.his, h]]);
      e = h + 5; stim(sc, 'base', e);
      const rb = rbUp('base', e), tc = h + 32; W_(sc, 'retro', rb, tc); down(sc, h, tc, h + 30);
      aExp = h + VIA.sep.dAP + 20; aNew = e + VIA.sep.dS.base + 15;
      W_(sc, 'retro', VIA.sep.paced('base', e)); W_(sc, 'retro', VIA.sep.desc(h), h + 70);
    } else {
      const n = a + NSLOW; W_(sc, 'ante', slowP(a, n)); hRef = E(sc, 'His', n + 30, 'H'); W_(sc, 'ante', [[G.node, n], [G.his, n + 30]]);
      e = n + 35; stim(sc, 'base', e);
      W_(sc, 'retro', rbUp('base', e), e + 40); down(sc, n + 30, n + 70, n + 70);
      aExp = aNew = fastUp(sc, n);
    }
    const prevA = a; a = aNew; if (trav) E(sc, 'AD', a, 'A');
    const tagA = sc.ev.find(x => x.ch === 'AD' && x.t === a);
    Object.assign(tagA, { tag: trav ? 'A adelantada' : 'A sin cambios', tagT: a + 1, tagUp: true });
    Object.assign(hRef, { tag: ' ', tagT: e + 1 });
    for (let i = 0; i < 4; i++) { b = trav ? travBeat(sc, a) : trnavBeat(sc, a); a = b.a; }
    brk(sc, 'AD', As[1], As[2], 'AA ' + (As[2] - As[1]), ); brk(sc, 'AD', prevA, aNew, 'AA ' + (aNew - prevA), { hot: 1 });
    const d = aExp - aNew;
    Object.assign(sc, { stimEnd: e, verdictT: aNew + 60,
      verdict: trav ? `La EV cae con el His ya activado y <b>adelanta la A ${d} ms</b> (AA ${aNew - prevA} en vez de ${LCT}), sin cambiar la secuencia: hay una vía y participa del circuito → <b>TRAV</b>.`
                    : `La EV cae con el His ya activado y <b>la A no cambia</b> (AA ${LCT}): el estímulo no tiene otro camino a la aurícula que el His, que está refractario.`,
      why: trav ? 'El estímulo de la base llega antes a la vía septal que el frente de la taquicardia, sube a la aurícula y la taquicardia sigue desde esa A adelantada (reset).'
                : 'El frente sube por la rama derecha y choca en el sistema de conducción. No excluye una vía espectadora ni una TA: excluye una vía que participe.' });
    return sc;
  }

  // Estimulación para-Hisiana en ritmo sinusal: salida alta (His + miocardio) y baja (solo miocardio)
  function parahisSc(mech) {
    const ap = mech === 'ap', sc = newSc({ title: ap ? 'Vía accesoria septal' : 'Conducción por el nodo', cats: ['ph'] });
    if (ap) sc.ap = 'sep';
    const S = [200, 800, 1400, 2000], R = [];
    S.forEach((s, i) => {
      const hi = i < 2; E(sc, 'ECG', s, 'E', { stim: true }); sc.flV.push(s + 10); sc.stims.push({ t: s, pt: G.ph, r: hi ? 30 : 15 });
      let h, A;
      if (hi) { h = s + 5; E(sc, 'His', h, 'H'); down(sc, h); E(sc, 'ECG', s + 20, '', { qrs: 'n' }); }
      else { h = s + 95; E(sc, 'His', h, 'H', { inv: true }); E(sc, 'ECG', s + 8, '', { qrs: 'w' });
        W_(sc, 'retro', [[G.ph, s], [[240, 420], s + 25], [[200, 515], s + 45], [G.rb4, s + 50], [G.rb3, s + 63], [G.rb2, s + 73], [G.rb1, s + 83], [G.his, h]]);
      }
      if (ap) { A = s + 70; W_(sc, 'retro', [[G.ph, s], [[258, 318], s + 20], [APS.sepV, s + 40], [APS.sep, s + 60], [[200, 215], s + 85], [G.ra, s + 105]]);
        W_(sc, 'retro', [[G.his, h], [G.node, h + 35]], Math.min(h + 35, A + 20)); E(sc, 'AD', A, 'A'); }
      else { W_(sc, 'retro', [[G.his, h], [G.node, h + 35]]); A = nodeUp(sc, h + 35); }
      R.push({ s, h, A });
    });
    const [, x, , y] = R;
    brk(sc, 'AD', x.s, x.A, 'SA ' + (x.A - x.s), { guide: 'ECG' }); brk(sc, 'AD', y.s, y.A, 'SA ' + (y.A - y.s), { guide: 'ECG', hot: 1 });
    brk(sc, 'His', x.s, x.h, 'SH ' + (x.h - x.s)); brk(sc, 'His', y.s, y.h, 'SH ' + (y.h - y.s), { hot: 1 });
    const dSA = (y.A - y.s) - (x.A - x.s), dSH = (y.h - y.s) - (x.h - x.s);
    sc.ev.find(e => e.ch === 'His' && e.t === y.h).tag = 'H retrógrado'; sc.ev.find(e => e.ch === 'His' && e.t === y.h).tagT = y.h + 1;
    Object.assign(sc, { stimEnd: 0, verdictT: y.A + 30, m: { R },
      verdict: ap ? `Al perder la captura del His el SH se alarga ${dSH} ms pero <b>el SA no cambia</b> (${x.A - x.s} ms): <b>conducción retrógrada por una vía accesoria</b>.`
                  : `Al perder la captura del His <b>el SA se alarga ${dSA} ms, lo mismo que el SH</b> (${dSH} ms): <b>conducción retrógrada por el nodo</b>.`,
      why: ap ? 'La vía se activa desde el miocardio vecino al catéter, capture o no el His. El HA se acorta (la A llega antes que el His retrógrado) y la secuencia auricular no cambia.'
              : 'La aurícula solo se alcanza a través del His: si el estímulo ya no lo captura directamente, tiene que bajar por el miocardio hasta el Purkinje y subir. El HA queda igual.' });
    return sc;
  }

  // Índice VA en ritmo sinusal: VA desde el ápex menos VA desde la base posterior
  function vaiSc(mech) {
    const ap = mech === 'ap', sc = newSc({ title: ap ? 'Vía posteroseptal' : 'Conducción por el nodo', cats: ['apex', 'base'] });
    if (ap) sc.ap = 'sep';
    const runs = [['apex', [300, 900, 1500]], ['base', [2300, 2900, 3500]]], va = {};
    runs.forEach(([site, S]) => S.forEach(s => {
      stim(sc, site, s); const rH = s + HR[site]; E(sc, 'His', rH, 'H', { inv: true }); let A;
      if (ap) { W_(sc, 'retro', VIA.sep.paced(site, s)); A = s + VIA.sep.dS[site] + 15; W_(sc, 'retro', rbUp(site, s), Math.min(rH + 35, A + 15)); E(sc, 'AD', A, 'A'); }
      else { W_(sc, 'retro', rbUp(site, s)); A = nodeUp(sc, rH + 35); }
      va[site] = { s, A };
    }));
    const vA = va.apex.A - va.apex.s, vB = va.base.A - va.base.s, idx = vA - vB;
    brk(sc, 'AD', va.apex.s, va.apex.A, 'VA ápex ' + vA, { guide: 'VD', hot: 1 }); brk(sc, 'AD', va.base.s, va.base.A, 'VA base ' + vB, { guide: 'VDb', hot: 1 });
    Object.assign(sc, { stimEnd: 0, verdictT: va.base.A + 30, m: { va },
      verdict: `Índice VA = VA ápex − VA base = ${vA} − ${vB} = <b>${sg(idx)} ms</b> → ${idx > 10 ? '<b>vía accesoria posteroseptal</b> (&gt; +10)' : '<b>conducción por el nodo</b> (negativo)'}.`,
      why: ap ? 'La base posterior está al lado de la inserción ventricular de la vía: desde ahí la A llega antes que desde el ápex.'
              : 'El nodo se alcanza por el His-Purkinje, que se entra cerca del ápex: desde la base el estímulo tiene que bajar hasta el Purkinje y subir, y el VA se alarga.' });
    return sc;
  }


  // ---------- Grupo 3: estimulación auricular y fármacos ----------
  const paceA = (sc, site, s, ch) => { E(sc, ch || 'AD', s, 'E', { stim: true }); sc.stims.push({ t: s, pt: G[site] }); };
  // TA focal: el foco dispara, la A conduce por el nodo (AH) y el His a los ventrículos
  const taBeat = (sc, f, ah, block) => { E(sc, 'AD', f, 'A'); W_(sc, 'focus', [[G.focus, f - 15], [[195, 195], f + 10], [G.aSep, f + 25]]);
    if (block) { W_(sc, 'ante', [[G.aSep, f + 25], [G.node, f + 25 + block]], f + 25 + block - 5); return null; }
    const h = f + ah; W_(sc, 'ante', [[G.aSep, f + 25], [G.node, f + 55], [G.his, h]]); E(sc, 'His', h, 'H'); down(sc, h); Vs(sc, h); return h; };

  // Sobreestimulación auricular durante la TSV: VA del primer latido de retorno (VA linking)
  function aopSc(mech) {
    const nav = mech === 'trnav', sc = newSc({ title: nav ? 'TRNAV típica' : 'Taquicardia auricular', cats: ['hra'] });
    let vaT, retV, retA, lastS, lastV, S = [];
    if (nav) {
      sc.nodal = true; let a = 120, b; E(sc, 'AD', a, 'A');
      for (let i = 0; i < 3; i++) { b = trnavBeat(sc, a); a = b.a; }
      vaT = b.a - (b.n + 75); const v0 = b.n + 75;
      let s = a + 300;
      for (let k = 0; k < 6; k++, s += 300) {
        paceA(sc, 'hra', s); S.push(s); E(sc, 'AD', s + 10, 'A'); W_(sc, 'ante', [[G.hra, s], [G.ra, s + 20], [G.aSep, s + 40]]);
        const n = s + 40 + NSLOW + 15; W_(sc, 'ante', slowP(s + 40, n)); E(sc, 'His', n + 30, 'H'); W_(sc, 'ante', [[G.node, n], [G.his, n + 30]]); down(sc, n + 30); Vs(sc, n + 30);
        if (k < 5) W_(sc, 'retro', [[G.node, n], [[252, 246], n + 30], [[232, 236], n + 55], [[200, 212], n + 75], [G.ra, n + 95]], n + 45);
        else { lastV = n + 75; retA = fastUp(sc, n); }
      }
      lastS = s - 300; a = retA; for (let i = 0; i < 3; i++) { b = trnavBeat(sc, a); a = b.a; }
      brk(sc, 'AD', v0 - 1, v0 + vaT, 'VA ' + vaT, { guide: 'VD' });
    } else {
      sc.focus = true; let f = 120, h;
      for (let i = 0; i < 3; i++, f += LCT) h = taBeat(sc, f, 120);
      vaT = LCT - 120 - HVT; const v0 = h + HVT;
      let s = f - LCT + 300;
      for (let k = 0; k < 6; k++, s += 300) {
        paceA(sc, 'hra', s); S.push(s); E(sc, 'AD', s + 10, 'A'); W_(sc, 'ante', [[G.hra, s], [G.ra, s + 20], [G.aSep, s + 40]]);
        const hh = s + 10 + 140; W_(sc, 'ante', [[G.aSep, s + 40], [G.node, s + 70], [G.his, hh]]); E(sc, 'His', hh, 'H'); down(sc, hh); Vs(sc, hh); lastV = hh + HVT;
      }
      lastS = s - 300; retA = lastS + 10 + 400;
      for (let i = 0; i < 4; i++) taBeat(sc, retA + i * LCT, 120);
      brk(sc, 'AD', v0, v0 + vaT, 'VA ' + vaT, { guide: 'VD' });
    }
    const vaR = retA - lastV, link = Math.abs(vaR - vaT) <= 10;
    brk(sc, 'AD', lastV, retA, 'VA ' + vaR, { guide: 'VD', hot: 1 });
    Object.assign(sc, { stimEnd: lastS, verdictT: retA + 30, m: { S, lastS },
      verdict: link ? `VA del primer retorno = ${vaR} ms, igual al VA de la TSV (${vaT}): <b>VA linking</b> → TRNAV o TRAV, <b>excluye la TA</b>.`
                    : `VA del primer retorno = ${vaR} ms, distinto del VA de la TSV (${vaT}; diferencia ${vaR - vaT} ms): <b>sin VA linking</b> → <b>TA</b>.`,
      why: nav ? 'La A de retorno sale del circuito, que gira en el nodo: siempre aparece a la misma distancia del V que la generó.'
               : 'La A de retorno la da el foco cuando vuelve a disparar, sin relación con el último V. Repetí desde otro sitio: en la TA el VA de retorno cambia (> 20 ms).' });
    return sc;
  }

  // EA con His refractario desde el ostium del SC: TRNAV vs taquicardia de la unión
  function ehaSc(mech) {
    const nav = mech === 'trnav', sc = newSc({ title: nav ? 'TRNAV típica' : 'Taquicardia de la unión (JET)', cats: ['cso'] });
    const Hs = []; let e, hNext, hExp;
    if (nav) {
      sc.nodal = true; let a = 120, b; E(sc, 'AD', a, 'A');
      for (let i = 0; i < 3; i++) { b = trnavBeat(sc, a); E(sc, 'CS', b.n + 60, 'A'); Hs.push(b.h); a = b.a; }
      // latido en el que entra el EA
      const n = a + NSLOW; W_(sc, 'ante', slowP(a, n)); const h = n + 30; E(sc, 'His', h, 'H'); Hs.push(h); W_(sc, 'ante', [[G.node, n], [G.his, h]]); down(sc, h); Vs(sc, h);
      W_(sc, 'retro', [[G.node, n], [[252, 246], n + 30], [[232, 236], n + 55]], n + 45);
      e = h + 2; paceA(sc, 'cso', e, 'CS'); E(sc, 'AD', e + 60, 'A'); W_(sc, 'ante', [[G.cso, e], [[168, 262], e + 30], [G.ra, e + 50], [G.hra, e + 65]]);
      // la vía rápida está refractaria (el His acaba de activarse): el EA no puede bajar por ella
      W_(sc, 'ante', [[G.cso, e], [[222, 264], e + 15], [[230, 240], e + 30]], e + 18);
      // entra por la vía lenta y baja con decremento: el His siguiente se retrasa
      sc.notes.push({ t0: e, t1: e + 260, x: 250, y: 208, txt: 'vía rápida refractaria', col: '#212121', anc: 'end' }, { t0: e + 20, t1: e + 340, x: 236, y: 340, txt: 'baja por la vía lenta', col: '#ef6c00', anc: 'end' });
      hExp = h + LCT; const n2 = e + 338; hNext = n2 + 30;
      W_(sc, 'ante', [[G.cso, e], [[220, 292], e + 40], [[236, 288], e + 130], [[250, 284], e + 240], [G.node, n2]]);
      E(sc, 'His', hNext, 'H'); W_(sc, 'ante', [[G.node, n2], [G.his, hNext]]); down(sc, hNext); Vs(sc, hNext); a = fastUp(sc, n2); E(sc, 'CS', n2 + 60, 'A');
      for (let i = 0; i < 3; i++) { b = trnavBeat(sc, a); E(sc, 'CS', b.n + 60, 'A'); a = b.a; }
    } else {
      sc.focus = true; sc.focusPt = G.jx;
      const jbeat = (f, cutR) => { E(sc, 'His', f, 'H'); W_(sc, 'focus', [[G.jx, f - 12], [G.his, f]]); down(sc, f); Vs(sc, f);
        W_(sc, 'retro', [[G.jx, f - 12], [G.node, f + 10], [G.aSep, f + 40], [G.ra, f + 70]], cutR); if (!cutR) { E(sc, 'AD', f + 65, 'A'); E(sc, 'CS', f + 40, 'A'); } };
      let f = 200; for (let i = 0; i < 4; i++, f += LCT) { jbeat(f); Hs.push(f); }
      const h = f; jbeat(f, f + 25); Hs.push(h);
      e = h + 2; paceA(sc, 'cso', e, 'CS'); E(sc, 'AD', e + 60, 'A'); W_(sc, 'ante', [[G.cso, e], [[168, 262], e + 30], [G.ra, e + 50], [G.hra, e + 65]]);
      W_(sc, 'ante', [[G.cso, e], [[250, 284], e + 20], [G.node, e + 35]], e + 28);
      hExp = hNext = h + LCT; for (let i = 0; i < 4; i++) jbeat(hNext + i * LCT);
    }
    const prevH = Hs[Hs.length - 1], d = hNext - hExp;
    brk(sc, 'His', Hs[Hs.length - 2], prevH, 'HH ' + (prevH - Hs[Hs.length - 2]), { up: 1 }); brk(sc, 'His', prevH, hNext, 'HH ' + (hNext - prevH), { hot: 1, up: 1 });
    Object.assign(sc, { stimEnd: e, verdictT: hNext + 30,
      verdict: nav ? `El EA cae con el His refractario y <b>retrasa el His siguiente ${d} ms</b> (HH ${hNext - prevH}): entró al circuito por la vía lenta → <b>TRNAV</b>.`
                   : `El EA cae con el His refractario y <b>el His siguiente llega a tiempo</b> (HH ${LCT}): no alcanzó el foco → <b>taquicardia de la unión</b>.`,
      why: nav ? 'La vía rápida está refractaria (el His acaba de activarse), así que el EA no puede bajar por ella. Entra por la vía lenta desde el ostium del SC y, como es precoz, conduce con decremento: el His siguiente se retrasa (también puede adelantarlo o terminar la TSV).'
               : 'El foco está en la unión, que acaba de activarse: el EA choca en el nodo refractario y no lo modifica.' });
    return sc;
  }

  // EA desde la pared lateral del AD durante una taquicardia preexcitada: antidrómica por vía atriofascicular vs TV
  function preexSc(mech) {
    const af = mech === 'af', sc = newSc({ title: af ? 'Antidrómica por vía atriofascicular' : 'TV con morfología de BRI', cats: ['ralat'] });
    const Vt = []; let e, vNext, vExp;
    if (af) {
      sc.ap = 'af';
      const cyc = (t, cutA) => { W_(sc, 'ante', [[G.afA, t], [[86, 360], t + 50], [[118, 460], t + 100], [G.afV, t + 140]]); const v = t + 150; E(sc, 'VD', v, 'V', { pre: 1 }); sc.flV.push(v); Vt.push(v);
        W_(sc, 'retro', [[G.afV, t + 140], [G.rb3, t + 158], [G.rb2, t + 168], [G.rb1, t + 180], [G.his, t + 195], [G.node, t + 225], [G.aSep, t + 285]]); E(sc, 'His', t + 195, 'H', { inv: true });
        W_(sc, 'retro', [[G.aSep, t + 285], [G.ra, t + 310], [G.ralat, t + 330], [G.afA, t + 340]], cutA); if (!cutA) E(sc, 'ADl', t + 330, 'A'); return t + 340; };
      let t = 100; E(sc, 'ADl', t - 10, 'A'); for (let i = 0; i < 3; i++) t = cyc(t);
      const tk = t; e = tk + 300; cyc(tk, tk + 305);       // en este ciclo el frente septal choca con el EA en la pared del AD
      paceA(sc, 'ralat', e, 'ADl'); E(sc, 'ADl', e + 5, 'A'); W_(sc, 'ante', [[G.ralat, e], [G.ra, e + 25]], e + 8);
      vExp = tk + LCT + 150; let t2 = cyc(e); vNext = e + 150; for (let i = 0; i < 3; i++) t2 = cyc(t2);
    } else {
      sc.focus = true; sc.focusPt = G.vtf;
      const vbeat = v => { W_(sc, 'focus', [[G.vtf, v - 20], [G.apex, v]]); E(sc, 'VD', v, 'V', { pre: 1 }); sc.flV.push(v); Vt.push(v);
        W_(sc, 'retro', [[G.vtf, v - 20], [G.rb3, v + 5], [G.rb2, v + 15], [G.rb1, v + 27], [G.his, v + 42], [G.node, v + 72]], v + 70); E(sc, 'His', v + 42, 'H', { inv: true }); };
      const sinus = a => { W_(sc, 'ante', [[G.sn, a - 30], [G.ralat, a], [G.ra, a + 10], [G.aSep, a + 35], [G.node, a + 60]], a + 55); E(sc, 'ADl', a, 'A'); };
      let v = 250; for (let i = 0; i < 5; i++, v += LCT) vbeat(v);
      [150, 750, 1350].forEach(sinus);
      e = Vt[3] + 160; paceA(sc, 'ralat', e, 'ADl'); E(sc, 'ADl', e + 5, 'A'); W_(sc, 'ante', [[G.ralat, e], [G.ra, e + 25], [G.aSep, e + 50], [G.node, e + 75]], e + 70);
      vExp = vNext = Vt[4]; for (let i = 0; i < 3; i++, v += LCT) vbeat(v);
    }
    const vPrev = Vt.filter(x => x < e).pop();
    brk(sc, 'VD', vPrev - LCT, vPrev, 'VV ' + LCT); brk(sc, 'VD', vPrev, vNext, 'VV ' + (vNext - vPrev), { hot: 1 });
    Object.assign(sc.ev.find(x => x.ch === 'VD' && x.t === vNext), { tag: af ? 'V adelantado' : 'V a tiempo', tagT: vNext + 1 });
    Object.assign(sc, { stimEnd: e, verdictT: vNext + 30,
      verdict: af ? `El EA lateral, con el septum ya activado, <b>adelanta el V siguiente ${vExp - vNext} ms con el mismo QRS</b> y la taquicardia sigue desde ahí: la vía es el brazo anterógrado y la aurícula está en el circuito → <b>antidrómica</b>.`
                  : `El EA lateral <b>no cambia el V siguiente</b> (VV ${LCT}): la aurícula no está conectada con el circuito → <b>TV</b> (o vía espectadora).`,
      why: af ? 'El EA entra a la vía atriofascicular por su inserción auricular en la pared libre antes que el frente de la taquicardia. Desde el septum no lo haría: por eso se compara pared libre vs septum.'
              : 'La aurícula va disociada (ritmo sinusal más lento) y el EA choca en un nodo refractario por la conducción retrógrada oculta del V.' });
    return sc;
  }

  // Adenosina durante la TSV: cómo termina o qué pasa si no termina
  function adoSc(mech) {
    const trav = mech === 'trav', sc = newSc({ title: trav ? 'TRAV por vía septal' : mech === 'trnav' ? 'TRNAV típica' : 'Taquicardia auricular', cats: [] });
    let tEnd, t0;
    if (mech === 'nv') {
      // vía nodoventricular: baja por el nodo y el His, sube por la vía al nodo; la aurícula es espectadora
      sc.title = 'Vía nodoventricular (NVRT)'; sc.ap = 'nv'; let n = 200; const plan = [30, 30, 30, 40, 45, 50], NVV = [250, 362];
      plan.forEach((hd, i) => { if (i === 3) t0 = n - 40; const h = n + hd, blockA = i >= 4; E(sc, 'His', h, 'H'); W_(sc, 'ante', [[G.node, n], [G.his, h]]); down(sc, h); Vs(sc, h);
        if (blockA) W_(sc, 'retro', [[G.node, n], [G.aSep, n + 35]], n + 12); else { W_(sc, 'retro', [[G.node, n], [G.aSep, n + 35], [G.ra, n + 70]]); E(sc, 'AD', n + 60, 'A'); }
        if (i === 4) Object.assign(sc.ev.find(x => x.ch === 'His' && x.t === h), { tag: 'sin A', tagT: h + 80 });
        const nn = h + 310, last = i === plan.length - 1; W_(sc, 'retro', [[NVV, h + 40], [[256, 318], h + 170], [G.node, nn]], last ? nn - 8 : null);
        if (last) tEnd = h + HVT; n = nn; });
      const s1 = tEnd + 1100; W_(sc, 'ante', [[G.sn, s1 - 30], [G.ra, s1], [G.aSep, s1 + 25], [G.node, s1 + 60], [G.his, s1 + 160]]); E(sc, 'AD', s1, 'A'); E(sc, 'His', s1 + 160, 'H'); down(sc, s1 + 160); Vs(sc, s1 + 160);
      sc.ado = [t0, tEnd + 500];
    } else if (mech === 'jet') {
      sc.title = 'JET con conducción VA 1:1'; sc.focus = true; sc.focusPt = G.jx; let f = 200;
      for (let i = 0; i < 10; i++, f += LCT) { const blockA = i >= 4 && i <= 6; if (i === 3) t0 = f - 40;
        E(sc, 'His', f, 'H'); W_(sc, 'focus', [[G.jx, f - 12], [G.his, f]]); down(sc, f); Vs(sc, f);
        if (blockA) W_(sc, 'retro', [[G.jx, f - 12], [G.node, f + 10], [G.aSep, f + 40]], f + 15); else { W_(sc, 'retro', [[G.jx, f - 12], [G.node, f + 10], [G.aSep, f + 40], [G.ra, f + 70]]); E(sc, 'AD', f + 65, 'A'); }
        if (i === 4) Object.assign(sc.ev.find(x => x.ch === 'His' && x.t === f), { tag: 'sin A', tagT: f + 80 }); }
      tEnd = 200 + 6 * LCT; sc.ado = [t0, 200 + 7 * LCT];
    } else if (mech === 'anti') {
      // antidrómica: baja por la vía atriofascicular y sube por la rama derecha, el His y el nodo
      sc.title = 'Antidrómica (vía atriofascicular)'; sc.ap = 'af'; let t = 100; const plan = [0, 0, 0, 20, 50, 'b'];
      plan.forEach((x, i) => { if (i === 3) t0 = t - 40;
        W_(sc, 'ante', [[G.afA, t], [[86, 360], t + 50], [[118, 460], t + 100], [G.afV, t + 140]]); const v = t + 150; E(sc, 'VD', v, 'V', { pre: 1 }); sc.flV.push(v);
        const up = [[G.afV, t + 140], [G.rb3, t + 158], [G.rb2, t + 168], [G.rb1, t + 180], [G.his, t + 195], [G.node, t + 225]]; E(sc, 'His', t + 195, 'H', { inv: true });
        if (x === 'b') { W_(sc, 'retro', up, t + 222); tEnd = v; Object.assign(sc.ev.find(e => e.ch === 'VD' && e.t === v), { tag: 'último V', tagT: v + 150 }); return; }
        const as = t + 285 + x; W_(sc, 'retro', up.concat([[G.aSep, as]])); W_(sc, 'retro', [[G.aSep, as], [G.ra, as + 25], [G.ralat, as + 45], [G.afA, as + 55]]); E(sc, 'AD', as + 25, 'A');
        t = as + 55; });
      const s1 = tEnd + 1100; W_(sc, 'ante', [[G.sn, s1 - 30], [G.ra, s1], [G.aSep, s1 + 25], [G.node, s1 + 60], [G.his, s1 + 160]]); E(sc, 'AD', s1, 'A'); E(sc, 'His', s1 + 160, 'H'); down(sc, s1 + 160); Vs(sc, s1 + 160);
      sc.ado = [t0, tEnd + 500];
    } else if (mech === 'trnav') {
      // la adenosina enlentece y después bloquea la vía lenta (brazo anterógrado): termina después de una A
      sc.nodal = true; let a = 120; E(sc, 'AD', a, 'A'); const dec = [0, 0, 0, 20, 50];
      dec.forEach((d, i) => { if (i === 3) t0 = a - 40; const n = a + NSLOW + d; W_(sc, 'ante', slowP(a, n)); E(sc, 'His', n + 30, 'H'); W_(sc, 'ante', [[G.node, n], [G.his, n + 30]]); down(sc, n + 30); Vs(sc, n + 30); a = fastUp(sc, n); });
      W_(sc, 'ante', slowP(a, a + NSLOW + 80), a + 200);
      Object.assign(sc.ev.find(x => x.ch === 'AD' && x.t === a), { tag: 'última A (no conduce)', tagT: a + 60 });
      tEnd = a; const s1 = a + 1100;
      W_(sc, 'ante', [[G.sn, s1 - 30], [G.ra, s1], [G.aSep, s1 + 25], [G.node, s1 + 60], [G.his, s1 + 160]]); E(sc, 'AD', s1, 'A'); E(sc, 'His', s1 + 160, 'H'); down(sc, s1 + 160); Vs(sc, s1 + 160);
      sc.ado = [t0, tEnd + 500];
    } else if (trav) {
      sc.ap = 'sep'; let a = 120; E(sc, 'AD', a, 'A'); const AHs = [185, 185, 185, 200, 230];
      AHs.forEach((ah, i) => { if (i === 3) t0 = a - 40; a = travBeat(sc, a, ah).a; });
      W_(sc, 'ante', [[G.aSep, a], [G.node, a + 40]], a + 35);
      Object.assign(sc.ev.find(x => x.ch === 'AD' && x.t === a), { tag: 'última A (no conduce)', tagT: a + 60 });
      tEnd = a; const s1 = a + 1100;
      W_(sc, 'ante', [[G.sn, s1 - 30], [G.ra, s1], [G.aSep, s1 + 25], [G.node, s1 + 60], [G.his, s1 + 160]]); E(sc, 'AD', s1, 'A'); E(sc, 'His', s1 + 160, 'H'); down(sc, s1 + 160); Vs(sc, s1 + 160);
      sc.ado = [t0, tEnd + 500];
    } else {
      sc.focus = true; let f = 120; const plan = [120, 120, 120, 150, 'b', 'b', 175, 'b', 140, 125, 120];
      plan.forEach((p, i) => { if (i === 3) t0 = f - 40; if (p === 'b') { taBeat(sc, f, 0, 30); const ev = sc.ev.find(x => x.ch === 'AD' && x.t === f); if (i === 4) Object.assign(ev, { tag: 'A bloqueada', tagT: f + 60 }); } else taBeat(sc, f, p); f += LCT; });
      tEnd = 120 + 5 * LCT; sc.ado = [t0, 120 + 8 * LCT];
    }
    Object.assign(sc, { stimEnd: 0, verdictT: tEnd + 200,
      verdict: mech === 'nv' ? 'Aparece <b>bloqueo VA y la taquicardia sigue</b> (desaparecen las A sin que cambie el ritmo ventricular): la aurícula no es parte del circuito. Después termina en el nodo, <b>con un V</b>.' : mech === 'jet' ? 'Las A desaparecen (<b>bloqueo VA</b>) y <b>el His y el V siguen igual</b> (HH 340): el foco está debajo del nodo → JET. Excluye la TRAV.' : mech === 'anti' ? 'La conducción retrógrada por el nodo se enlentece (el VA se alarga) y la taquicardia <b>termina con un V, sin A</b>: el nodo era el brazo retrógrado.' : mech === 'trnav' ? 'La vía lenta se enlentece (el AH se alarga) y la taquicardia <b>termina con una A que no conduce</b>: el bloqueo es en la vía lenta (brazo anterógrado) → TRNAV o TRAV, <b>excluye la TA</b>.'
             : trav ? 'El AH se alarga y la taquicardia <b>termina con una A que no conduce</b> (bloqueo en el nodo): TRNAV o TRAV, <b>excluye la TA</b>.'
                    : 'Aparece <b>bloqueo AV y las A siguen</b> a la misma LC: la aurícula no necesita al nodo → <b>TA</b> (excluye la TRAV).',
      why: mech === 'nv' ? 'Lo que la separa de la TRAV es el bloqueo VA con la TSV que sigue (la TRAV no puede seguir sin la A). Lo mismo puede verse en la TRNAV con bloqueo del haz común superior y en la JET.' : mech === 'jet' ? 'La adenosina bloquea el nodo, que acá es solo el camino hacia la aurícula: el foco de la unión sigue disparando. Cuando pasa el efecto vuelve la conducción VA 1:1.' : mech === 'anti' ? 'Ojo: la vía atriofascicular también es sensible a la adenosina (conduce como un nodo), así que puede terminar después de una A, bloqueando la vía. Si el brazo retrógrado es otra vía accesoria, la adenosina no la corta.' : mech === 'trnav' ? 'Las dos vías del nodo son el circuito. Lo habitual es que se bloquee la vía lenta después de la A; si se bloquea la rápida (retrógrada), termina con un V, que no discrimina. Después vuelve el sinusal.'
             : trav ? 'El nodo es un brazo del circuito: al bloquearse, el circuito se corta. Después vuelve el ritmo sinusal.'
                : 'La adenosina bloquea el nodo, que no es parte del circuito: el foco sigue disparando y se ve mientras dura el bloqueo.' });
    return sc;
  }


  // ---------- Grupo 4: observaciones y estudio basal ----------
  // vía lateral izquierda: latido de la TRAV desde la A del SC distal (a). bri: bloqueo funcional de la rama izquierda
  const travLat = (sc, a, bri) => {
    W_(sc, 'retro', [[G.apA, a], [G.la, a + 15], [[380, 250], a + 30], [G.aSep, a + 40]]); W_(sc, 'retro', [[G.apA, a], [[520, 200], a + 30]]);
    E(sc, 'CSd', a, 'A'); E(sc, 'CSp', a + 30, 'A'); E(sc, 'His', a + 40, 'A');
    const h = a + 185; W_(sc, 'ante', [[G.aSep, a + 40], [G.node, a + 70], [G.his, h]]); E(sc, 'His', h, 'H');
    const [r, l] = ramas(h, HVT); W_(sc, 'ante', r.pts);
    let lv = h + HVT;
    if (bri) { W_(sc, 'ante', l.pts, h + 6); W_(sc, 'ante', [[G.rb2, h + 22], [[330, 430], h + 50], [[390, 425], h + 68], [G.lvA, lv = h + 85]]); E(sc, 'VD', h + HVT, 'V', { pre: 1 }); }
    else { W_(sc, 'ante', l.pts); E(sc, 'VD', h + HVT, 'V'); }
    sc.flV.push(h + HVT);
    W_(sc, 'retro', [[G.lvA, lv], [G.lvB, lv + 40], [G.apV, lv + 95], [G.apA, lv + 110]]);
    return { h, v: h + HVT, a: lv + 110 };
  };

  function basalSc(kind) {
    const sc = newSc({ cats: [] });
    if (kind === 'trnav') {
      Object.assign(sc, { title: 'TRNAV típica: VA septal corto y activación concéntrica', nodal: true, cats: ['cs'] });
      let a = 120, b; for (let i = 0; i < 5; i++) { b = trnavBeat(sc, a); E(sc, 'His', b.n + 90, 'A'); E(sc, 'CSp', b.n + 95, 'A'); E(sc, 'CSd', b.n + 125, 'A'); a = b.a; if (i === 2) sc.m.b = b; }
      const v = sc.m.b.n + 75; brk(sc, 'His', v, v + 15, 'VA 15', { guide: 'VD', hot: 1, up: 1 });
      Object.assign(sc, { verdictT: v + 200, verdict: 'VA septal <b>15 ms</b> (≤ 70) y la A más precoz en el His, después el SC proximal y por último el distal (<b>concéntrica</b>): patrón de TRNAV típica; <b>excluye la TRAV</b>.',
        why: 'La A sale del nodo casi al mismo tiempo que el V. En la TRAV la A necesita que el impulso recorra el ventrículo y cruce la vía: el VA no puede ser tan corto (en niños, &lt; 60 ms la excluye).' });
    } else if (kind === 'travl' || kind === 'coumel') {
      Object.assign(sc, { title: kind === 'coumel' ? 'TRAV por vía lateral izquierda con BRI funcional' : 'TRAV por vía lateral izquierda: activación excéntrica', ap: 'lat', cats: ['cs'] });
      let a = 150, b; const R = [];
      const plan = kind === 'coumel' ? [0, 0, 0, 1, 1, 1, 0, 0] : [0, 0, 0, 0, 0];
      plan.forEach(x => { b = travLat(sc, a, x); R.push(Object.assign({ a0: a, bri: x }, b)); a = b.a; });
      if (kind === 'travl') { const r = R[2]; brk(sc, 'CSd', r.v, r.a, 'VA ' + (r.a - r.v), { guide: 'VD', hot: 1, up: 1 }); brk(sc, 'His', r.v, r.a + 40, 'VA ' + (r.a + 40 - r.v), { guide: 'VD', up: 1 });
        Object.assign(sc, { verdictT: r.a + 300, verdict: 'A más precoz en el <b>SC distal</b> (VA 110 ms), después el proximal y por último el His (150 ms): activación <b>excéntrica</b> → TRAV por vía izquierda (o TA izquierda); <b>excluye la TRNAV</b> (salvo la rara variante izquierda).',
          why: 'La A sale por la inserción auricular de la vía, en la pared lateral del AI, y desde ahí avanza hacia el septum.' }); }
      else { const n = R[2], w = R[4]; brk(sc, 'CSd', n.v, n.a, 'VA ' + (n.a - n.v), { guide: 'VD', up: 1 }); brk(sc, 'CSd', w.v, w.a, 'VA ' + (w.a - w.v), { guide: 'VD', hot: 1, up: 1 });
        brk(sc, 'VD', R[1].v, R[2].v, 'VV ' + (R[2].v - R[1].v)); brk(sc, 'VD', R[4].v, R[5].v, 'VV ' + (R[5].v - R[4].v), { hot: 1 });
        sc.m.bri = R[3].v;
        Object.assign(sc, { verdictT: R[5].v + 60, verdict: `Con BRI funcional el VA se alarga <b>${(w.a - w.v) - (n.a - n.v)} ms</b> (${n.a - n.v} → ${w.a - w.v}) y la LC también (${R[2].v - R[1].v} → ${R[5].v - R[4].v}): la vía izquierda es parte del circuito (<b>efecto Coumel</b>).`,
          why: 'Con la rama izquierda bloqueada el frente baja por la derecha y cruza el septum hasta el VI: tarda más en llegar a la vía. Un aumento > 20–30 ms prueba una vía libre homolateral al bloqueo.' }); }
    } else {
      Object.assign(sc, { title: 'Taquicardia auricular con bloqueo AV', focus: true });
      let f = 120; const plan = [120, 120, 120, 150, 180, 'b', 120, 150, 'b', 120];
      plan.forEach((p, i) => { if (p === 'b') { taBeat(sc, f, 0, 30); if (i === 5) Object.assign(sc.ev.find(x => x.ch === 'AD' && x.t === f), { tag: 'A sin V', tagT: f + 40 }); } else taBeat(sc, f, p); f += LCT; });
      brk(sc, 'AD', 120 + 4 * LCT, 120 + 5 * LCT, 'AA 340'); brk(sc, 'AD', 120 + 5 * LCT, 120 + 6 * LCT, 'AA 340', { hot: 1 });
      Object.assign(sc, { verdictT: 120 + 6 * LCT, verdict: 'Una A no conduce (Wenckebach) y <b>la taquicardia sigue igual</b> (AA 340): no necesita al ventrículo → <b>TA o TRNAV</b>; <b>excluye la TRAV</b>.',
        why: 'En la TRAV cada A necesita el V anterior: un bloqueo AV la termina. Es más frecuente en la TA, pero por prevalencia muchas veces es una TRNAV con bloqueo en el haz común inferior.' });
    }
    return sc;
  }

  // Estudio basal: doble vía nodal con extraestímulos auriculares
  function dualSc() {
    const sc = newSc({ title: 'Extraestímulos auriculares: salto del AH', nodal: true, cats: ['hra'] });
    const fast = (a, ah) => { W_(sc, 'ante', [[G.hra, a - 10], [G.ra, a + 10], [[232, 234], a + 30], [[252, 246], a + 50], [G.node, a + ah - 30], [G.his, a + ah]]); };
    const slow = (a, ah) => { W_(sc, 'ante', [[G.hra, a - 10], [G.ra, a + 10], [[226, 248], a + 30], [[206, 268], a + 90], [[220, 292], a + 140], [[250, 284], a + ah - 60], [G.node, a + ah - 30], [G.his, a + ah]]); };
    const beat = (s, ah, viaSlow, mk) => { paceA(sc, 'hra', s); const a = s + 10; E(sc, 'AD', a, 'A'); (viaSlow ? slow : fast)(a, ah); const h = a + ah; E(sc, 'His', h, 'H'); down(sc, h); Vs(sc, h);
      if (viaSlow) W_(sc, 'ante', [[G.ra, a + 10], [[232, 234], a + 30], [[252, 246], a + 45]], a + 40); return { a, h }; };
    const P = [[400, 130], [320, 150], [280, 240]], R = [];
    let t = 200;
    P.forEach(([c, ah], i) => { beat(t, 100); const x = beat(t + c, ah, ah > 200); R.push(Object.assign({ c }, x)); brk(sc, 'His', x.a, x.h, 'A2H2 ' + ah, { hot: i === 2, up: 1 }); t += 1300; });
    sc.m.R = R;
    Object.assign(sc, { stimEnd: 0, verdictT: R[2].h + 30, verdict: 'Al acortar el acoplamiento 40 ms el A2H2 <b>salta 90 ms</b> (150 → 240): la vía rápida quedó refractaria y conduce la lenta → <b>doble fisiología nodal</b> (salto ≥ 50 ms).',
      why: 'A favor de TRNAV (VPP 86 %), pero solo muestra el sustrato: puede ser espectador.' });
    return sc;
  }

  // Estudio basal: estimulación ventricular incremental, VA por el nodo vs por una vía lateral izquierda
  function vaPaceSc(mech) {
    const ap = mech === 'ap', sc = newSc({ title: ap ? 'Conducción VA por una vía lateral izquierda' : 'Conducción VA por el nodo', cats: ['apex', 'cs'] });
    if (ap) sc.ap = 'lat';
    const PCL = [600, 600, 450, 450, 350, 350, 300, 300], R = []; let s = 200;
    PCL.forEach((c, i) => { stim(sc, 'apex', s); const rH = s + HR.apex; E(sc, 'His', rH, 'H', { inv: true });
      let a;
      if (ap) { a = s + 140; W_(sc, 'retro', [[G.apex, s], [[260, 600], s + 30], [[400, 560], s + 70], [[500, 430], s + 105], [G.apV, s + 125], [G.apA, a]]);
        W_(sc, 'retro', [[G.apA, a], [G.la, a + 15], [[380, 250], a + 30], [G.aSep, a + 40]]); W_(sc, 'retro', rbUp('apex', s), rH + 25);
        E(sc, 'CSd', a, 'A'); E(sc, 'CSp', a + 30, 'A'); E(sc, 'His', a + 40, 'A'); }
      else { const dec = [0, 0, 20, 20, 50, 50, 90, 'b'][i];
        if (dec === 'b') { W_(sc, 'retro', rbUp('apex', s), rH + 30); R.push({ s, a: null }); s += c; return; }
        W_(sc, 'retro', rbUp('apex', s)); const tn = rH + 35 + dec; W_(sc, 'retro', [[G.node, rH + 35], [G.node, tn], [G.aSep, tn + 40], [G.ra, tn + 85]]);
        a = tn + 60; E(sc, 'His', a, 'A'); E(sc, 'CSp', a + 8, 'A'); E(sc, 'CSd', a + 35, 'A'); }
      R.push({ s, a, c }); s += c; });
    const ref = ap ? 'CSd' : 'His', fA = r => ap ? r.a : r.a;
    [1, 3, 5].forEach((k, j) => brk(sc, ref, R[k].s, fA(R[k]), 'VA ' + (fA(R[k]) - R[k].s), { guide: 'VD', hot: j === 2, up: 1 }));
    if (!ap) Object.assign(sc.ev.find(x => x.ch === 'His' && x.t === R[7].s + HR.apex), { tag: 'sin A', tagT: R[7].s + 200 });
    Object.assign(sc, { stimEnd: 0, verdictT: R[7].s + 250,
      verdict: ap ? 'Al acortar la LC el <b>VA no cambia</b> (140 ms) y la A más precoz está en el <b>SC distal</b>: conducción <b>no decremental y excéntrica</b> → vía accesoria lateral izquierda.'
                  : `Al acortar la LC el <b>VA se alarga</b> (${[1, 3, 5].map(k => R[k].a - R[k].s).join(' → ')} ms) hasta que aparece <b>bloqueo VA</b>, con la A más precoz en el His: conducción <b>decremental y concéntrica</b> → nodo.`,
      why: ap ? 'El tejido de la vía conduce como el miocardio: no tiene decremento. Ojo: las vías decrementales (PJRT) se comportan como el nodo.'
              : 'El nodo conduce con decremento. Un bloqueo VA con LC larga (&gt; 600 ms) va en contra de una vía y también de la TRNAV.' });
    return sc;
  }

  // Doble disparo nodal: una A, dos His y dos V
  function dfireSc() {
    const sc = newSc({ title: 'Taquicardia no reentrante por doble vía nodal', nodal: true, cats: [] });
    const R = [];
    [150, 950, 1750, 2550].forEach(a => {
      W_(sc, 'ante', [[G.sn, a - 40], [G.ra, a - 10], [G.aSep, a + 15]]); E(sc, 'AD', a, 'A');
      const h1 = a + 120, h2 = h1 + 360;
      W_(sc, 'ante', [[G.aSep, a + 15], [[232, 234], a + 30], [[252, 246], a + 55], [G.node, a + 90], [G.his, h1]]); E(sc, 'His', h1, 'H'); down(sc, h1); Vs(sc, h1);
      W_(sc, 'ante', [[[226, 248], a + 25], [[206, 268], a + 120], [[220, 292], a + 230], [[250, 284], a + 330], [G.node, h2 - 30], [G.his, h2]]); E(sc, 'His', h2, 'H'); down(sc, h2); Vs(sc, h2);
      R.push({ a, h1, h2 }); });
    brk(sc, 'His', R[1].h1, R[1].h2, 'H1–H2 360', { up: 1 }); brk(sc, 'His', R[2].h1, R[2].h2, 'H1–H2 360', { hot: 1, up: 1 });
    Object.assign(sc, { stimEnd: 0, verdictT: R[2].h2 + 60, m: { R },
      verdict: 'Cada A sinusal da <b>dos His y dos V</b> (A-H1-V1-H2-V2), con <b>H1–H2 fijo</b> (360 ms) y el mismo HV: <b>doble disparo nodal</b>. No es una reentrada.',
      why: 'La misma A baja por la vía rápida y, cientos de ms después, por la lenta (que no quedó bloqueada). Se ve como una P y dos QRS angostos; se confunde con FA o extrasístoles. Se trata con ablación de la vía lenta.' });
    return sc;
  }

  // Nodos AV gemelos
  function twinSc(kind) {
    const sc = newSc({ title: kind === 'tsv' ? 'TRAV por nodos AV gemelos' : 'Estimulación auricular desde dos sitios', twin: true, cats: kind === 'tsv' ? [] : ['hra', 'cso'] });
    const NP = [226, 304], HP = [276, 376];
    if (kind === 'tsv') {
      let a = 120; const R = [];
      for (let i = 0; i < 5; i++) {
        const h = a + 100; W_(sc, 'ante', [[G.aSep, a], [G.node, a + 30], [G.his, h]]); E(sc, 'AD', a + 10, 'A'); E(sc, 'His', h, 'H'); down(sc, h); Vs(sc, h); E(sc, 'ECG', h + 20, '', { qrs: 'n' });
        const hp = h + 95; W_(sc, 'retro', [[G.rb1, h + 18], [[282, 380], h + 30], [HP, h + 60], [NP, hp + 35], [G.cso, hp + 75], [G.aSep, hp + 145]]); E(sc, 'HisP', hp, 'H', { inv: true });
        R.push({ a, h, hp }); a = hp + 145; }
      brk(sc, 'AD', R[2].a + 10, R[3].a + 10, 'AA ' + (R[3].a - R[2].a), { hot: 1 });
      Object.assign(sc, { stimEnd: 0, verdictT: R[3].h + 60, verdict: 'Baja por el nodo anterior (His anterior antes del V, QRS angosto) y <b>sube por el nodo posterior</b> (His posterior retrógrado, A más precoz cerca del ostium del SC): <b>TRAV por nodos gemelos</b>.',
        why: 'Es un circuito AV con dos sistemas de conducción, como una TRAV con una "vía" que en realidad es otro nodo: decremental y sensible a la adenosina. Encarrilando desde los dos sitios nodales el PPI es corto.' });
    } else {
      const R = [];
      [[200, 'hra'], [900, 'hra'], [1700, 'cso'], [2400, 'cso']].forEach(([s, site]) => {
        paceA(sc, site, s); E(sc, 'AD', s + (site === 'hra' ? 10 : 40), 'A');
        if (site === 'hra') { const h = s + 130; W_(sc, 'ante', [[G.hra, s], [G.ra, s + 20], [G.aSep, s + 40], [G.node, s + 70], [G.his, h]]); E(sc, 'His', h, 'H'); down(sc, h); Vs(sc, h); E(sc, 'ECG', h + 20, '', { qrs: 'n' }); R.push(h); }
        else { const hp = s + 110; W_(sc, 'ante', [[G.cso, s], [NP, s + 40], [HP, hp]]); W_(sc, 'ante', [[HP, hp], [G.rb2, hp + 20], [G.rb3, hp + 35], [G.apex, hp + 50]]); W_(sc, 'ante', [[HP, hp], [[330, 430], hp + 25], [G.lvA, hp + 50]]);
          W_(sc, 'ante', [[G.cso, s], [G.aSep, s + 25], [G.node, s + 50]], s + 45);
          E(sc, 'HisP', hp, 'H'); E(sc, 'VD', hp + 40, 'V'); sc.flV.push(hp + 40); E(sc, 'ECG', hp + 15, '', { qrs: 'm' }); R.push(hp); } });
      Object.assign(sc, { stimEnd: 0, verdictT: R[3] + 80, verdict: 'Desde la AD alta conduce el <b>nodo anterior</b> (His anterior, QRS 1); desde el ostium del SC, el <b>nodo posterior</b> (His posterior, QRS 2). <b>Dos QRS distintos no preexcitados</b>, cada uno con su His: dos sistemas de conducción AV.',
        why: 'Así se demuestran en 2 de cada 3 pacientes (estimulación auricular diferencial). En el 93 % hay heterotaxia (sobre todo isomerismo derecho); también en la TCGA y el canal AV malalineado.' });
    }
    return sc;
  }

  // Vía oblicua lateral izquierda: vista ampliada del anillo mitral (aurícula arriba, ventrículo abajo, SC en el medio).
  // Los canales del SC van de distal (1-2, lateral) a proximal (7-8, septal).
  const CSX = { C12: [512, 292], C34: [450, 300], C56: [380, 304], C78: [300, 302] }, OBA = [446, 268], OBV = [516, 316];
  const RX = { C78: 110, C56: 230, C34: 350, C12: 460 }, RAI = [330, 118], RVI = [470, 186];
  function oblSc(kind) {
    const retro = kind === 'retro', sc = newSc({ title: retro ? 'Conducción retrógrada (estimulación ventricular)' : 'Conducción anterógrada (ritmo sinusal, preexcitado)', view: 'ring', vb: kind === 'rev' ? '0 0 560 325' : '0 0 560 320', cats: [], fronts: [] });
    const R = [], r = Math.round;
    const local = (lane, t, l) => E(sc, lane, r(t), l);
    const vBeat = (s, lat) => {
      const v0 = s + 62, kV = 0.1, tV = x => v0 + (lat ? 530 - x : x - 30) * kV;
      const tVI = tV(RVI[0]), tAI = tVI + 15, kA = 0.15, tA = x => tAI + Math.abs(x - RAI[0]) * kA;
      sc.fronts.push({ band: 'V', x0: lat ? 530 : 30, t0: v0, k: kV, dir: lat ? 'left' : 'right' }, { band: 'A', x0: RAI[0], t0: tAI, k: kA, dir: 'both' });
      sc.stims.push({ t: s + 50, pt: lat ? [520, 225] : [40, 225] });
      W_(sc, 'retro', [[RVI, tVI], [RAI, tAI]]); sc.flA.push(tAI); sc.flV.push(v0);
      for (const k in RX) { local(k, tV(RX[k]), 'V'); local(k, tA(RX[k]), 'A'); }
      local('C12', tVI + 15 * (RVI[0] - RX.C12) / (RVI[0] - RAI[0]), 'P'); local('C34', tVI + 15 * (RVI[0] - RX.C34) / (RVI[0] - RAI[0]), 'P');
      return { s, tV, tA, tAI, lat };
    };
    if (kind === 'rev') {
      sc.title = 'Invertir el frente ventricular (Otomo 2001)';
      [300, 1000].forEach(t => R.push(vBeat(t, false))); [1800, 2500].forEach(t => R.push(vBeat(t, true)));
      const va = x => r(x.tA(RX.C34)) - r(x.tV(RX.C34)), [a, b] = [R[1], R[3]];
      brk(sc, 'C34', r(a.tV(RX.C34)), r(a.tA(RX.C34)), 'VA ' + va(a), { up: 1 }); brk(sc, 'C34', r(b.tV(RX.C34)), r(b.tA(RX.C34)), 'VA ' + va(b), { hot: 1, up: 1 });
      sc.notes.push({ t0: 250, t1: 1700, x: 280, y: 312, txt: 'frente ventricular: septal → lateral', col: '#ef6c00', anc: 'middle' }, { t0: 1700, t1: 99999, x: 280, y: 312, txt: 'frente ventricular: lateral → septal', col: '#ef6c00', anc: 'middle' });
      Object.assign(sc, { stimEnd: 0, verdictT: b.s + 200, m: { R },
        verdict: `Al invertir el frente ventricular el <b>VA local en 3-4</b> (la A más precoz) pasa de <b>${va(a)} a ${va(b)} ms</b>: cambia ≥ 15 ms, así que la vía es <b>oblicua</b>. Con el frente lateral → septal el V cae casi encima de la A y tapa el potencial de la vía; con el septal → lateral se separan y el potencial (P) se ve.`,
        why: 'Con el frente en el mismo sentido que la conducción por la vía, el ventrículo debajo de la inserción auricular se activa tarde, casi junto con la A. En el sentido contrario se activa temprano y queda separado. Otomo 2001: el VA local aumentó ≥ 15 ms en el 91 % de las vías y, mapeando con el VA largo, se encontró el potencial en el 89 %.' });
    } else if (retro) {
      [300, 1000, 1700].forEach(t => R.push(vBeat(t, false)));         // el frente ventricular llega desde el septum
      const x = R[1], va34 = r(x.tA(RX.C34)) - r(x.tV(RX.C34)), va12 = r(x.tA(RX.C12)) - r(x.tV(RX.C12));
      brk(sc, 'C34', r(x.tV(RX.C34)), r(x.tA(RX.C34)), 'VA ' + va34, { hot: 1, up: 1 }); brk(sc, 'C12', r(x.tV(RX.C12)), r(x.tA(RX.C12)), 'VA ' + va12, { up: 1 });
      sc.notes.push({ t0: r(x.tA(RX.C34)), t1: 99999, x: RX.C34, y: 104, txt: 'A más precoz', col: '#6a3fb5', anc: 'middle' });
      Object.assign(sc, { stimEnd: 0, verdictT: x.s + 200, m: { R },
        verdict: `El frente ventricular viene del septum, pasa por debajo de 3-4 y recién entra a la vía en su <b>inserción ventricular</b> (1-2). Sube en diagonal y sale en la <b>inserción auricular</b> (3-4): ahí está la <b>A más precoz</b> (VA local ${va34} ms en 3-4, ${va12} ms en 1-2). Entre el V y la A se registra el <b>potencial de la vía</b> (P).`,
        why: 'La A más precoz marca la inserción auricular, no el lugar donde la vía toma al ventrículo. Comparala con el V más precoz de la conducción anterógrada.' });
    } else {
      [200, 900, 1600].forEach(a => {
        const a0 = a - 10, kA = 0.13, tA = x => a0 + (x - 30) * kA;          // el frente auricular sinusal llega desde el septum
        const tAI = tA(RAI[0]), tVI = tAI + 30, kV = 0.12, tV = x => tVI + Math.abs(x - RVI[0]) * kV;
        sc.fronts.push({ band: 'A', x0: 30, t0: a0, k: kA, dir: 'right' }, { band: 'V', x0: RVI[0], t0: tVI, k: kV, dir: 'both' });
        W_(sc, 'ante', [[RAI, tAI], [RVI, tVI]]); sc.flA.push(a0); sc.flV.push(tVI);
        for (const k in RX) { local(k, tA(RX[k]), 'A'); local(k, tV(RX[k]), 'V'); }
        local('C34', tAI + 30 * (RX.C34 - RAI[0]) / (RVI[0] - RAI[0]), 'P'); local('C12', tAI + 30 * (RX.C12 - RAI[0]) / (RVI[0] - RAI[0]), 'P');
        R.push({ a, tA, tV });
      });
      const x = R[1], av12 = r(x.tV(RX.C12)) - r(x.tA(RX.C12)), av34 = r(x.tV(RX.C34)) - r(x.tA(RX.C34));
      brk(sc, 'C12', r(x.tA(RX.C12)), r(x.tV(RX.C12)), 'AV ' + av12, { hot: 1, up: 1 }); brk(sc, 'C34', r(x.tA(RX.C34)), r(x.tV(RX.C34)), 'AV ' + av34, { up: 1 });
      sc.notes.push({ t0: r(x.tV(RX.C12)), t1: 99999, x: RX.C12, y: 252, txt: 'V más precoz', col: '#ef6c00', anc: 'middle' });
      Object.assign(sc, { stimEnd: 0, verdictT: x.a + 130, m: { R },
        verdict: `El frente auricular viene del septum y entra a la vía en su <b>inserción auricular</b> (3-4). Baja en diagonal y sale en la <b>inserción ventricular</b> (1-2): ahí está el <b>V más precoz</b> (AV local ${av12} ms en 1-2, ${av34} ms en 3-4). El potencial de la vía (P) va ahora de 3-4 a 1-2.`,
        why: 'En la conducción retrógrada la A más precoz está en 3-4; en la anterógrada, el V más precoz está en 1-2. Esa separación (4–30 mm, mediana 14–15 mm en las libres izquierdas) es la oblicuidad: el blanco más preciso es el potencial de la vía.' });
    }
    return sc;
  }


  // ---------- Grupo 5: taquicardias ventriculares ----------
  const LPF0 = [312, 334], LPFm = [346, 432], LPFl = [370, 476], LPFb = [400, 520], P1t = [314, 384], P1m = [328, 442], P1b = [350, 502];
  const sinusDown = (sc, h, hv, opt) => { const o = opt || {}; E(sc, 'His', h, 'H'); W_(sc, 'ante', [[G.node, h - 30], [G.his, h]]); down(sc, h); E(sc, 'VD', h + hv, 'V'); sc.flV.push(h + hv); if (o.ecg) E(sc, 'ECG', h + hv - 5, '', { qrs: o.ecg }); };

  // Reentrada rama-rama típica: sube por la rama izquierda y baja por la derecha
  function bbrSc(kind) {
    const sc = newSc({ title: kind === 'ppi' ? 'Rama-rama: encarrilamiento desde el ápex del VD' : 'Reentrada rama-rama típica (BRI)', bbr: true, cats: kind === 'ppi' ? ['apex'] : [] });
    const R = [];
    const rbDown = (t, cut) => W_(sc, 'ante', [[G.his, t], [G.rb1, t + 20], [G.rb2, t + 35], [G.rb3, t + 50], [G.rb4, t + 62], [G.apex, t + 70]], cut);
    const cyc = (t, slow, noV) => { E(sc, 'His', t, 'H'); E(sc, 'RB', t + 20, 'RB'); rbDown(t);
      const v = t + 70; E(sc, 'VD', v, 'V'); E(sc, 'ECG', v - 8, '', { qrs: 'w' }); sc.flV.push(v);
      W_(sc, 'ante', [[G.apex, v], [[300, 560], v + 30], [LPFb, v + 70]]);
      const up = 270 + (slow || 0); W_(sc, 'retro', [[LPFb, v + 80], [LPFm, v + 150 + (slow || 0) / 2], [LPF0, v + up - 20], [G.his, v + up]]);
      R.push({ t, v }); return v + up; };
    // latido sinusal con HV largo y QRS ancho de base
    const hs = 150; sinusDown(sc, hs, 60, { ecg: 'w' }); E(sc, 'RB', hs + 15, 'RB');
    brk(sc, 'VD', hs, hs + 60, 'HV 60', { guide: 'His' });
    if (kind === 'ppi') {
      let t = 700; for (let i = 0; i < 3; i++) t = cyc(t);
      let s = R[2].v + 300; const S = [];
      for (let k = 0; k < 5; k++, s += 300) { stim(sc, 'apex', s); S.push(s); W_(sc, 'retro', [[G.apex, s], [[300, 560], s + 30], [LPFb, s + 70]]);
        W_(sc, 'retro', [[LPFb, s + 80], [LPFm, s + 150], [LPF0, s + 265], [G.his, s + 285]]); E(sc, 'His', s + 285, 'H'); E(sc, 'RB', s + 305, 'RB');
        rbDown(s + 285, k < 4 ? s + 320 : null); }
      const last = S[4], tr = last + 285; let t2 = cyc(tr); for (let i = 0; i < 2; i++) t2 = cyc(t2);
      const retV = tr + 70, ppi = retV - last;
      brk(sc, 'VD', last, retV, 'PPI ' + ppi, { hot: 1 }); brk(sc, 'VD', R[0].v, R[1].v, 'LC ' + (R[1].v - R[0].v));
      Object.assign(sc, { stimEnd: last, verdictT: retV + 40, m: { S },
        verdict: `PPI − LC = ${ppi} − ${LCT} = <b>${ppi - LCT} ms</b> (≤ 30): el ápex del VD, donde sale la rama derecha, está en el circuito → <b>rama-rama</b>.`,
        why: 'En una TV miocárdica el ápex del VD suele estar lejos del circuito: PPI−LC > 30 ms. El tratamiento es la ablación de la rama derecha.' });
    } else {
      let t = 700; t = cyc(t); t = cyc(t); t = cyc(t, 30); t = cyc(t); cyc(t);
      brk(sc, 'VD', R[1].t, R[1].t + 70, 'HV 70', { guide: 'His', hot: 1 });
      brk(sc, 'His', R[2].t, R[3].t, 'HH ' + (R[3].t - R[2].t), { up: 1, hot: 1 }); brk(sc, 'RB', R[2].v, R[3].v, 'VV ' + (R[3].v - R[2].v), { hot: 1 });
      Object.assign(sc, { stimEnd: 0, verdictT: R[3].v + 40, m: { R },
        verdict: 'El <b>His y la rama derecha preceden a cada V</b>, con HV igual o mayor que en sinusal (70 vs 60 ms), y cuando el ciclo oscila <b>el HH cambia antes que el VV</b> (370 → 370): el His-Purkinje gobierna la taquicardia → <b>rama-rama</b>.',
        why: 'Sube por la rama izquierda (violeta) y baja por la derecha (naranja): QRS con BRI, a menudo igual al sinusal. Ojo con el His pasivo de una TV miocárdica (VH largo, disociación VH intermitente).' });
    }
    return sc;
  }

  // TV fascicular posterior: baja por P1 (Purkinje anormal, lento) y sube por el fascículo posterior (P2)
  function tvfSc(kind) {
    const sc = newSc({ title: kind === 'vera' ? 'TV fascicular posterior: verapamilo' : kind === 'abl' ? 'TV fascicular posterior: ablación en P2' : 'TV fascicular posterior (P1 y P2)', fasc: true, cats: kind === 'abl' ? ['abl'] : [] });
    if (kind === 'abl') sc.ablPt = LPFl;   // P2 presistólico más precoz, en el fascículo posterior distal (sitio de salida)
    const R = [];
    const cyc = (t0, span, block, turn) => {
      const tr = turn || 10;
      if (block === 'turn') { W_(sc, 'ante', [[P1t, t0], [P1m, t0 + span / 2], [P1b, t0 + span], [LPFb, t0 + span + 60]], t0 + span + 25); E(sc, 'LV', t0 + span / 2, 'P1'); R.push({ t0, span, block: true }); return null; }
      W_(sc, 'ante', [[P1t, t0], [P1m, t0 + span / 2], [P1b, t0 + span]], block ? t0 + span * 0.75 : null); E(sc, 'LV', t0 + span / 2, 'P1');
      if (block) { R.push({ t0, span, block: true }); return null; }
      const b = t0 + span + tr, qrs = b + 25; W_(sc, 'ante', [[P1b, t0 + span], [LPFb, b]]);
      W_(sc, 'retro', [[LPFb, b], [LPFl, b + 10], [LPFm, b + 25], [LPF0, b + 42], [G.his, b + 50]]); E(sc, 'LV', b + 10, 'P2'); E(sc, 'His', b + 50, 'H', { inv: true });
      W_(sc, 'ante', [[LPFb, b + 10], [[440, 560], b + 50]]); W_(sc, 'ante', [[LPFb, b + 10], [[300, 560], b + 55], [G.apex, b + 75]]);
      E(sc, 'ECG', qrs, '', { qrs: 'w' }); sc.flV.push(qrs);
      W_(sc, 'retro', [[LPFm, b + 25], [P1t, b + 50]]);
      R.push({ t0, span, b, qrs }); return b + 50; };
    let t = 150, spans = kind === 'circ' ? [300, 300, 300, 300, 300] : [300, 300, 300, 340, 390, 'b'];
    if (kind === 'abl') { [10, 10, 10, 35, 70].forEach(tr => { t = cyc(t, 300, false, tr); }); cyc(t, 300, 'turn'); }
    else spans.forEach((sp, i) => { if (sp === 'b') { cyc(t, 420, true); return; } t = cyc(t, sp); });
    const c = R[1];
    brk(sc, 'LV', c.t0 + c.span / 2, c.b + 10, 'P1–P2 ' + (c.b + 10 - (c.t0 + c.span / 2)), { up: 1 }); brk(sc, 'LV', c.b + 10, c.qrs, 'P2–QRS ' + (c.qrs - c.b - 10), { below: 1 });
    if (kind === 'circ') {
      Object.assign(sc, { stimEnd: 0, verdictT: R[3].qrs + 40,
        verdict: '<b>P1</b> mesodiastólico (baja por el Purkinje anormal, lento) y <b>P2</b> presistólico (sube por el fascículo posterior) en el septum medio; el His se activa <b>después</b> del inicio del QRS, en sentido retrógrado: <b>TV fascicular posterior</b>.',
        why: 'El frente sale al miocardio cerca del fascículo posterior distal: QRS con BRD y eje superior. P1 es parte crítica del circuito.' });
    } else {
      const last = R[R.length - 2], blk = R[R.length - 1];
      brk(sc, 'LV', last.t0 + last.span / 2, last.b + 10, 'P1–P2 ' + (last.b + 10 - (last.t0 + last.span / 2)), { up: 1, hot: 1 });
      const tEnd = blk.t0 + 210;
      // ritmo sinusal después
      const hs = tEnd + 700; sinusDown(sc, hs, 45, { ecg: 'n' });
      if (kind === 'abl') { W_(sc, 'ante', [[G.his, hs], [LPF0, hs + 8], [LPFm, hs + 25], [LPFl, hs + 35]], hs + 30); E(sc, 'LV', hs + 75, 'P2', { tag: 'P2 tardío', tagT: hs + 90 }); }
      else { W_(sc, 'ante', [[G.his, hs], [LPF0, hs + 8], [LPFm, hs + 25], [LPFb, hs + 40]]); E(sc, 'LV', hs + 25, 'P2'); }
      if (kind === 'abl') { sc.rf = [R[2].t0 + 150, tEnd + 300, LPFl]; }
      Object.assign(sc, { stimEnd: tEnd, verdictT: tEnd + 60,
        verdict: kind === 'vera' ? 'El verapamilo <b>alarga P1–P2</b> (y la LC) <b>sin cambiar P2–QRS</b>, hasta que la conducción se bloquea dentro de P1 y la TV termina.'
                                 : 'Durante la RF en el <b>P2 presistólico más precoz</b> (sitio de salida, en el fascículo posterior distal), <b>P1–P2 se alarga</b> y la TV termina con un P1 que no llega a P2: el giro inferior del circuito quedó bloqueado. Después, en sinusal, el fascículo posterior se bloquea en el sitio de ablación y <b>P2 aparece tarde</b>.',
        why: kind === 'vera' ? 'P1 es tejido de Purkinje anormal, decremental y sensible al verapamilo: es el brazo lento del circuito.'
                             : 'Es el blanco cuando no se registra P1. El bloqueo fascicular posterior izquierdo nuevo en el ECG (eje derecho) sirvió como punto final (38 de 39 sin recurrencia, Ma 2006). Ojo: en el septum basal hay riesgo de BRI y BAV transitorios.' });
    }
    return sc;
  }




  // ---------- Grupo 6: reset y encarrilamiento sobre un circuito esquemático ----------
  // Anillo de reentrada: 0° arriba, sentido horario. LC 340 ms; período refractario 230 ms (brecha excitable 110 ms).
  const LC6 = 340, RF6 = 230, W6 = 360 / LC6, RC = [280, 178], RR = 112;
  const rpos = a => [RC[0] + RR * Math.sin(a * Math.PI / 180), RC[1] - RR * Math.cos(a * Math.PI / 180)];
  const nrm = a => ((a % 360) + 360) % 360;
  // tiempo de la última activación de un punto del anillo por una onda, hasta T
  const actT = (w, a, T) => { if (T < w.t0) return null; const d = nrm((a - w.a0) * w.dir); let t = w.t0 + d / W6; const lim = Math.min(T, w.t1);
    if (t > lim) return null; if (w.dir > 0) t += Math.floor((lim - t) / LC6) * LC6; return t; };
  const headA = (w, T) => nrm(w.a0 + w.dir * W6 * (T - w.t0));
  const passes = (w, a) => { const out = []; let t = w.t0 + nrm((a - w.a0) * w.dir) / W6; while (t <= w.t1) { out.push(t); if (w.dir < 0) break; t += LC6; } return out; };

  function loopSc(kind) {
    const out = kind === 'out', reset = kind === 'reset';
    const sc = newSc({ title: reset ? 'Reset con un extraestímulo' : out ? 'Encarrilamiento desde fuera del circuito' : 'Encarrilamiento desde el circuito (istmo protegido)', view: 'loop', vb: '0 0 560 360', cats: [], loop: [] });
    const PS = 90, PX = 160, PE = 90, SOUT = [500, 300], DST = 60;        // sitio de estimulación, salida, entrada desde fuera
    sc.loopSite = out ? SOUT : rpos(PS); sc.loopEntry = out ? rpos(PE) : null; sc.loopExit = rpos(PX);
    const L = sc.loop; const nat = { a0: 0, dir: 1, t0: -LC6 * 3, t1: 1e9, k: 'o' }; L.push(nat);
    const pa = out ? PE : PS, dIn = out ? DST : 0;                           // punto del anillo donde entra el estímulo y demora
    const collide = (prev, ts) => { const g = nrm(pa - headA(prev, ts)); return ts + g / (2 * W6); };
    const S = [];
    if (reset) { const lastAct = actT(nat, pa, 1000); const ts = lastAct + 265; S.push(ts); }
    else { const first = actT(nat, pa, 900) + 250 - dIn; for (let k = 0; k < 6; k++) S.push(first + k * 300); }
    let prev = nat;
    S.forEach((s, k) => { const ta = s + dIn; const tc = collide(prev, ta); prev.t1 = tc;
      L.push({ a0: pa, dir: -1, t0: ta, t1: tc, k: 'a' }); const o = { a0: pa, dir: 1, t0: ta, t1: 1e9, k: 'o' }; L.push(o); prev = o;
      E(sc, 'S', s, 'E', { stim: true }); sc.stims.push({ t: s, pt: sc.loopSite });
      if (out) W_(sc, 'ante', [[SOUT, s], [rpos(PE), ta]]); });
    const lastS = S[S.length - 1];
    // electrogramas: salida (cada vez que pasa el frente ortodrómico) y sitio de estimulación
    const exits = []; L.filter(w => w.k === 'o').forEach(w => passes(w, PX).forEach(t => { if (t > 0 && t < lastS + 1400) exits.push(t); }));
    exits.sort((a, b) => a - b);
    exits.forEach(t => { E(sc, 'X', t, 'V'); const pacing = !reset && t > S[0] && t < lastS + 60; E(sc, 'ECG', t + 20, '', { qrs: out && pacing ? 'm' : 'w' }); sc.flV.push(t); });
    const siteActs = []; L.filter(w => w.k === 'o').forEach(w => passes(w, pa).forEach(t => { if (t > 0 && t > w.t0 + 1 && t < lastS + 1400) siteActs.push(t); }));
    if (!out) siteActs.forEach(t => { if (!S.some(s => Math.abs(s - t) < 2)) E(sc, 'S', t, 'V'); });
    const ret = (out ? passes(prev, PE).find(t => t > lastS + dIn + 1) + DST : passes(prev, PS).find(t => t > lastS + 1));
    if (out) { W_(sc, 'retro', [[rpos(PE), ret - DST], [SOUT, ret]]); E(sc, 'S', ret, 'V'); }
    sc.m = { S, exits, ret };
    if (reset) {
      const s = S[0], before = exits.filter(t => t < s).pop(), after = exits.find(t => t > s), expected = before + LC6;
      brk(sc, 'X', before - LC6, before, 'LC ' + LC6, { up: 1 }); brk(sc, 'X', before, after, 'VV ' + Math.round(after - before), { up: 1, hot: 1 });
      Object.assign(sc, { stimEnd: s, verdictT: after + 60,
        verdict: `El extraestímulo cae en la <b>brecha excitable</b>: el frente antidrómico choca con el que viene y el ortodrómico sigue por el circuito. La salida siguiente se <b>adelanta ${Math.round(expected - after)} ms</b> y la pausa es menos que compensadora: <b>reset</b>.`,
        why: 'Solo se puede resetear una reentrada si tiene brecha excitable (el tejido delante del frente ya se recuperó). Después del reset la taquicardia sigue con su LC, desde el nuevo frente.' });
    } else {
      const ppi = Math.round(ret - lastS);
      brk(sc, 'S', lastS, ret, 'PPI ' + ppi, { hot: 1, up: 1 });
      const lastPure = exits.find(t => t > lastS);
      if (out) { const q = sc.ev.find(e => e.ch === 'ECG' && Math.abs(e.t - lastPure - 20) < 1); if (q) Object.assign(q, { tag: 'sin fusión', tagT: lastPure + 30 }); }
      Object.assign(sc, { stimEnd: lastS, verdictT: ret + 40,
        verdict: out ? `Desde fuera del circuito el estímulo tiene que llegar al circuito, dar la vuelta y volver: <b>PPI ${ppi} ms</b>, PPI − LC = <b>${ppi - LC6} ms</b>. Durante la estimulación hay <b>fusión constante</b> (el frente estimulado sale también por fuera del circuito) y el último latido no tiene fusión.`
                     : `Desde el circuito, el frente ortodrómico da una vuelta y vuelve al sitio en una LC: <b>PPI = ${ppi} ms</b> (PPI − LC = <b>${ppi - LC6}</b>). En un istmo protegido el QRS no cambia (<b>encarrilamiento oculto</b>).`,
        why: out ? 'El PPI − LC es el doble del tiempo de conducción entre el sitio y el circuito: cuanto más lejos, más largo. Es lo que se usa en el PPI − LC desde el VD.'
                 : 'Cada estímulo genera un frente antidrómico que choca con el ortodrómico anterior y uno ortodrómico que sigue: la taquicardia se acelera a la LC de estimulación y, al cortar, retoma su LC.' });
    }
    return sc;
  }

  // PPI−LC, SA−VA y ΔHA: un mismo encarrilamiento con un selector de medición (cada ficha arranca con la suya)
  const ENTM = { ppi: ['PPI − LC', 'Medí el <b>PPI</b> en el canal del VD: de la última espiga al primer V de retorno, y restale la LC.'],
    sava: ['SA − VA', 'Medí el <b>SA</b>: de la última espiga a la A del último latido acelerado, y comparalo con el <b>VA</b> de la TSV.', 'Antes de estimular, mirá el <b>VA</b> de la TSV (del V a la A).'],
    dha: ['ΔHA', 'Medí el <b>HA</b> del último latido estimulado (del His retrógrado a la A) y comparalo con el HA de la TSV.', 'Antes de estimular, mirá el <b>HA</b> de la TSV (del His a la A).'],
    all: ['Las tres', 'Las tres mediciones salen del mismo encarrilamiento: PPI en el canal del VD, SA y VA en la AD alta y HA en el His.', 'Antes de estimular, mirá la LC, el VA y el HA de la TSV.'] };
  const ANIMS = {
    vop: { t: 'Sobreestimulación ventricular: A-V vs A-A-V', n: 'Sobreestimulación ventricular', dur: 4200, panels: [travVop, taVop],
      fases: s => s[0].focus
        ? [[0, 'Taquicardia auricular (LC 340 ms): el foco dispara y cada A conduce por el nodo. Mirá las A, H y V en el trazado.'],
           [850, 'Estimulación del VD a 300 ms (E): cada estímulo sube por la rama, el His y el nodo, y las A se aceleran a 300.'],
           [2100, 'Se corta la estimulación. Mirá qué sigue a la <b>última A acelerada</b>.'],
           [3000, 'El foco vuelve a disparar y la taquicardia retoma su ciclo (LC 340).']]
        : [[0, 'TRAV (LC 340 ms): baja por el nodo y sube por la vía. Mirá el circuito en el esquema y las A, H y V en el trazado.'],
           [690, 'Estimulación del VD a 300 ms (E): cada estímulo sube por la vía y las A se aceleran a 300.'],
           [2100, 'Se corta la estimulación. Mirá qué sigue a la <b>última A acelerada</b>.'],
           [3000, 'La taquicardia retoma su ciclo (LC 340): el frente vuelve a girar por el nodo, el ventrículo y la vía.']] },
    ppi: entA('ppi'), sava: entA('sava'), dha: entA('dha'),
    hisorto: { t: 'Captura ortodrómica del His', n: 'Captura ortodrómica del His', panels: [() => hisorto(320), () => hisorto(270)],
      fases: s => [[0, 'TRAV (LC 340 ms), encarrilada desde el ápex del VD. Mirá cómo y cuándo se activa el His.'],
        [s[0].m.runs[0].S[0] - 10, s[0].ortho ? 'Estimulación del VD a 320 ms, 20 ms menos que la LC (lo más lento posible).' : 'Estimulación del VD a 270 ms, 70 ms menos que la LC.'],
        [s[0].m.runs[0].S[3], s[0].ortho ? 'Seguí el His: baja desde el nodo (naranja) y choca con el estímulo en la rama derecha.' : 'Seguí el His: el estímulo sube primero por la rama derecha (violeta) y lo activa desde abajo.'],
        [s[0].stimEnd + 200, 'Al cortar, la taquicardia sigue igual.']] },
    diff: { t: 'Encarrilamiento diferencial: ápex vs base', n: 'Encarrilamiento diferencial', lanes: [['AD', 'AD alta'], ['His', 'His'], ['VDb', 'VD base'], ['VD', 'VD ápex']], panels: [() => diffSc('trav'), () => diffSc('trnav')],
      fases: s => { const [a, b] = s[0].m.runs; return [[0, 'Taquicardia. Hay un catéter en el ápex del VD y otro en la base, cerca del His.'],
        [a.S[0] - 10, 'Primero se encarrila desde el <b>ápex</b> (a 300 ms).'], [a.lastS + 1, 'Medí el VA (espiga → A) y el PPI desde el ápex.'],
        [b.S[0] - 10, 'Ahora se encarrila desde la <b>base</b>, a la misma LC.'], [b.lastS + 1, 'Medí el VA y el PPI desde la base y restá: base − ápex.']]; } },
    ehr: { t: 'EV con His refractario: TRAV vs TRNAV', n: 'EV con His refractario', dur: 2500, lanes: [['AD', 'AD alta'], ['His', 'His'], ['VDb', 'VD base']], panels: [() => ehrSc('trav'), () => ehrSc('trnav')],
      fases: s => { const e = s[0].stimEnd; return [[0, 'Taquicardia (LC 340 ms). Hay un catéter en la base del VD, cerca de la vía septal.'],
        [e - 60, 'Mirá el His: se activa en forma anterógrada. Desde ese momento el His está refractario.'],
        [e - 4, 'Se da <b>una sola EV</b> desde la base del VD, justo después del His (His refractario). El frente no puede subir por el His.'],
        [e + 110, 'Mirá la A siguiente: ¿llega antes de lo esperado (AA &lt; 340) o a tiempo?'],
        [e + 450, s[0].ap ? 'Después de la EV la taquicardia sigue desde la A adelantada (se reseteó).' : 'Después de la EV la taquicardia sigue igual, sin cambios.']]; } },
    parahis: { t: 'Estimulación para-Hisiana: nodo vs vía septal', n: 'Estimulación para-Hisiana', win: 2600, lanes: [['ECG', 'ECG'], ['AD', 'AD alta'], ['His', 'His']], panels: [() => parahisSc('node'), () => parahisSc('ap')],
      fases: s => { const R = s[0].m.R; return [[0, 'Ritmo sinusal. El catéter está en la región del His.'],
        [R[0].s - 10, '<b>Salida alta</b>: se captura el His y el miocardio vecino. QRS angosto y His inmediato (SH corto).'],
        [R[2].s - 10, '<b>Salida baja</b>: se captura solo el miocardio. QRS ancho (BRI) y aparece el His retrógrado, más tarde (SH largo).'],
        [R[3].s + 1, 'Compará el <b>SA</b> con y sin captura del His (y la secuencia auricular).']]; } },
    aop: { t: 'Sobreestimulación auricular: VA linking', n: 'Sobreestimulación auricular', panels: [() => aopSc('trnav'), () => aopSc('ta')],
      fases: s => { const m = s[0].m; return [[0, s[0].nodal ? 'TRNAV típica (LC 340 ms): baja por la vía lenta y sube por la rápida.' : 'Taquicardia auricular (LC 340 ms): el foco dispara y conduce por el nodo.'],
        [m.S[0] - 10, 'Estimulación de la AD alta a 300 ms (E): confirmá que el V se acelera a 300.'],
        [m.lastS + 1, 'Se corta la estimulación. Medí el <b>VA del primer latido de retorno</b> y comparalo con el VA de la TSV.']]; } },
    eha: { t: 'EA con His refractario: TRNAV vs unión', n: 'EA con His refractario', lanes: [['AD', 'AD alta'], ['CS', 'SC ostium'], ['His', 'His'], ['VD', 'VD']], panels: [() => ehaSc('trnav'), () => ehaSc('jet')],
      fases: s => { const e = s[0].stimEnd; return [[0, 'Taquicardia (LC 340 ms) con A y V casi simultáneos. Catéter en el ostium del SC, en la región de la vía lenta.'],
        [e - 40, 'Mirá el His: se activa ahora, así que el His (la vía rápida) queda refractario.'],
        [e - 1, 'Se da <b>un EA</b> desde el ostium del SC <b>en el momento del His</b>.'], [e + 150, 'Mirá el <b>His siguiente</b>: ¿se retrasa, se adelanta o llega a tiempo?']]; } },
    preex: { t: 'EA en taquicardia preexcitada: antidrómica vs TV', n: 'EA en taquicardia preexcitada', lanes: [['ADl', 'AD lateral'], ['His', 'His'], ['VD', 'VD ápex']], panels: [() => preexSc('af'), () => preexSc('vt')],
      fases: s => { const e = s[0].stimEnd; return [[0, 'Taquicardia de QRS ancho con morfología de BRI (LC 340 ms). Catéter en la pared lateral del AD.'],
        [e - 60, 'El septum y la unión AV ya se activaron (están refractarios).'],
        [e - 1, 'Se da <b>un EA</b> desde la pared lateral del AD.'], [e + 120, 'Mirá el <b>V siguiente</b>: ¿se adelanta con el mismo QRS?']]; } },
    ...Object.fromEntries([['trav', 'TRAV'], ['trnav', 'TRNAV típica'], ['ta', 'taquicardia auricular'], ['nv', 'taquicardia por vía nodoventricular'], ['jet', 'taquicardia de la unión (JET) con VA 1:1'], ['anti', 'TRAV antidrómica']].map(([m, n]) =>
      ['ado_' + m, { t: 'Adenosina en la ' + n, panels: [() => adoSc(m)], dur: 3700, win: 3000,
        fases: s => [[0, 'Taquicardia (LC 340 ms). Se inyecta adenosina.'], [s[0].ado[0], 'La adenosina llega al nodo (azul).'],
          [s[0].ado[0] + 700, 'Mirá <b>cómo termina</b>, o qué pasa con las A si no termina.']] }])),
    basal_trnav: { t: 'Observaciones: VA septal y secuencia en la TRNAV típica', lanes: [['CSd', 'SC dist'], ['CSp', 'SC prox'], ['His', 'His'], ['VD', 'VD']], panels: [() => basalSc('trnav')],
      fases: s => [[0, 'TRNAV típica (LC 340 ms). Mirá dónde aparece primero la A: His, SC proximal o SC distal.'], [s[0].m.b.n + 70, 'Medí el <b>VA septal</b>: del inicio del V a la A del His.']] },
    basal_travl: { t: 'Observaciones: activación excéntrica en la TRAV por vía izquierda', lanes: [['CSd', 'SC dist'], ['CSp', 'SC prox'], ['His', 'His'], ['VD', 'VD']], panels: [() => basalSc('travl')],
      fases: s => [[0, 'TRAV por una vía lateral izquierda (LC 340 ms). Mirá dónde aparece primero la A.'], [800, 'Medí el VA en el SC distal y en el His.']] },
    basal_ta: { t: 'Observaciones: TA que sigue con bloqueo AV', panels: [() => basalSc('ta')],
      fases: s => [[0, 'Taquicardia auricular (LC 340 ms).'], [120 + 3 * LCT, 'El AH se alarga de a poco (Wenckebach)...'], [120 + 5 * LCT, '...y una A no conduce. ¿Sigue la taquicardia?']] },
    basal_coumel: { t: 'Observaciones: efecto Coumel (BRI funcional)', lanes: [['CSd', 'SC dist'], ['CSp', 'SC prox'], ['His', 'His'], ['VD', 'VD']], panels: [() => basalSc('coumel')], win: 2400,
      fases: s => [[0, 'TRAV por una vía lateral izquierda con QRS angosto. Medí el VA y la LC.'], [s[0].m.bri - 60, 'Aparece <b>BRI funcional</b>: el frente ya no baja por la rama izquierda y el QRS se ensancha.'], [s[0].m.bri + 700, 'Compará el VA y la LC con y sin BRI.']] },
    pre_dual: { t: 'Estudio basal: doble fisiología nodal', panels: [dualSc], win: 1400, gap: 50,
      fases: s => { const R = s[0].m.R; return [[0, 'Ritmo sinusal. Se estimula la AD alta: un latido de base (S1) y un extraestímulo (S2), cada vez más precoz.'], [R[0].a - 5, 'Acoplamiento 400 ms: el S2 baja por la vía rápida.'], [R[1].a - 5, '320 ms: sigue por la rápida y el AH se alarga un poco.'], [R[2].a - 5, '280 ms: la vía rápida está refractaria y el S2 baja por la <b>vía lenta</b>.']]; } },
    pre_vanode: { t: 'Estudio basal: conducción VA por el nodo', lanes: [['CSd', 'SC dist'], ['CSp', 'SC prox'], ['His', 'His'], ['VD', 'VD']], panels: [() => vaPaceSc('node')], win: 2600,
      fases: s => [[0, 'Se estimula el VD con LC cada vez más cortas (600, 450, 350 y 300 ms).'], [1300, 'Mirá cómo cambia el VA y dónde aparece primero la A.']] },
    pre_vaap: { t: 'Estudio basal: conducción VA por una vía accesoria', lanes: [['CSd', 'SC dist'], ['CSp', 'SC prox'], ['His', 'His'], ['VD', 'VD']], panels: [() => vaPaceSc('ap')], win: 2600,
      fases: s => [[0, 'Se estimula el VD con LC cada vez más cortas (600, 450, 350 y 300 ms).'], [1300, 'Mirá cómo cambia el VA y dónde aparece primero la A.']] },
    dfire: { t: 'Doble disparo nodal (respuesta 1:2)', panels: [dfireSc], win: 2600,
      fases: s => { const R = s[0].m.R; return [[0, 'Ritmo sinusal. Mirá cuántos His y V salen de cada A.'], [R[0].h1 - 60, 'La A baja por la <b>vía rápida</b>: H1 y V1...'], [R[0].h1 + 80, '...y la misma A sigue bajando por la <b>vía lenta</b>: H2 y V2.']]; } },
    twin_tsv: { t: 'Nodos AV gemelos: la taquicardia', lanes: [['ECG', 'ECG'], ['AD', 'AD alta'], ['His', 'His ant.'], ['HisP', 'His post.']], panels: [() => twinSc('tsv')],
      fases: [[0, 'Paciente con heterotaxia: dos nodos AV (anterior y posterior), cada uno con su His. Mirá por dónde baja y por dónde sube la taquicardia.']] },
    twin_ap: { t: 'Nodos AV gemelos: estimulación auricular diferencial', lanes: [['ECG', 'ECG'], ['AD', 'AD alta'], ['His', 'His ant.'], ['HisP', 'His post.']], panels: [() => twinSc('ap')], win: 2600,
      fases: [[0, 'Ritmo sinusal. Se estimula primero la AD alta...'], [1650, '...y después el ostium del SC: conduce el otro nodo.']] },
    obl_retro: { t: 'Vía oblicua: conducción retrógrada', win: 260, dur: 1270, lanes: [['C12', 'SC 1-2'], ['C34', 'SC 3-4'], ['C56', 'SC 5-6'], ['C78', 'SC 7-8']], panels: [() => oblSc('retro')],
      fases: s => { const R = s[0].m.R[0]; return [[0, 'Vista ampliada del anillo mitral: aurícula arriba, ventrículo abajo y el catéter del SC en el medio. Se estimula el VD.'], [R.s + 55, 'Seguí el <b>frente ventricular</b> (naranja): llega desde el septum y pasa por debajo de 3-4 sin activar la vía.'], [R.tAI - 32, 'Entra a la vía en la <b>inserción ventricular</b> (1-2), sube en diagonal (violeta) y sale en la <b>inserción auricular</b> (3-4).'], [R.tAI + 5, 'Desde la inserción auricular la aurícula se activa hacia los dos lados: la <b>A más precoz</b> está en 3-4.']]; } },
    obl_rev: { t: 'Vía oblicua: invertir el frente de estimulación', win: 260, dur: 2770, lanes: [['C12', 'SC 1-2'], ['C34', 'SC 3-4'], ['C56', 'SC 5-6'], ['C78', 'SC 7-8']], panels: [() => oblSc('rev')],
      fases: [[0, 'La misma vía. Primero se estimula el ventrículo del lado <b>septal</b>: el frente ventricular va de septal a lateral.'], [1050, 'Medí el VA local en 3-4 (la A más precoz): V, potencial de la vía y A bien separados.'],
        [1700, 'Ahora se estimula del lado <b>lateral</b>: el frente ventricular va al revés, de lateral a septal.'], [2550, 'Medí de nuevo el VA local en 3-4: el V cae casi encima de la A.']] },
    obl_ante: { t: 'Vía oblicua: conducción anterógrada', win: 260, dur: 1100, lanes: [['C12', 'SC 1-2'], ['C34', 'SC 3-4'], ['C56', 'SC 5-6'], ['C78', 'SC 7-8']], panels: [() => oblSc('ante')],
      fases: s => { const R = s[0].m.R[0]; return [[0, 'Vista ampliada del anillo mitral. Ritmo sinusal con preexcitación por la misma vía.'], [R.a - 10, 'Seguí el <b>frente auricular</b> (violeta): llega desde el septum y entra a la vía en la <b>inserción auricular</b> (3-4).'], [R.a + 25, 'Baja por la vía en diagonal (naranja) y sale en la <b>inserción ventricular</b> (1-2).'], [R.a + 55, 'Desde la inserción ventricular el ventrículo se activa hacia los dos lados: el <b>V más precoz</b> está en 1-2.']]; } },
    bbr_tv: { t: 'Reentrada rama-rama: criterios en la taquicardia', lanes: [['His', 'His'], ['RB', 'Rama der.'], ['VD', 'VD'], ['ECG', 'ECG']], panels: [() => bbrSc('tv')], win: 1800,
      fases: [[0, 'Ritmo sinusal con HV largo (60 ms) y QRS ancho: trastorno de la conducción de base.'], [650, 'Taquicardia: sube por la <b>rama izquierda</b> (violeta) y baja por la <b>derecha</b> (naranja). Mirá el His y la rama antes de cada V.'], [1600, 'El ciclo oscila: mirá si cambia primero el HH o el VV.']] },
    bbr_ppi: { t: 'Reentrada rama-rama: encarrilamiento desde el ápex', lanes: [['His', 'His'], ['RB', 'Rama der.'], ['VD', 'VD'], ['ECG', 'ECG']], panels: [() => bbrSc('ppi')], win: 1800,
      fases: s => { const S = s[0].m.S; return [[0, 'Ritmo sinusal y después la taquicardia rama-rama (LC 340 ms).'], [S[0] - 10, 'Se encarrila desde el <b>ápex del VD</b> a 300 ms: el estímulo entra al circuito por la salida de la rama derecha.'], [S[4] + 1, 'Se corta. Medí el <b>PPI</b> en el VD y restale la LC.']]; } },
    tvf_circ: { t: 'TV fascicular posterior: P1 y P2', lanes: [['His', 'His'], ['LV', 'Septo VI'], ['ECG', 'ECG']], panels: [() => tvfSc('circ')], win: 1500,
      fases: [[0, 'TV fascicular posterior (LC 360 ms). El circuito está en el septum del VI: baja por <b>P1</b> (Purkinje anormal, lento, línea punteada) y sube por el <b>fascículo posterior</b> (P2).'], [500, 'Mirá en el septo: P1 en la mitad de la diástole y P2 justo antes del QRS. El His se activa después del inicio del QRS.']] },
    tvf_vera: { t: 'TV fascicular posterior: efecto del verapamilo', lanes: [['His', 'His'], ['LV', 'Septo VI'], ['ECG', 'ECG']], panels: [() => tvfSc('vera')], win: 1600,
      fases: s => [[0, 'TV fascicular posterior (LC 360 ms).'], [1100, 'Se da <b>verapamilo</b>: P1 conduce cada vez más lento.'], [s[0].stimEnd - 200, 'Medí P1–P2 y P2–QRS: ¿qué intervalo se alarga?'], [s[0].stimEnd, 'La conducción se bloquea dentro de P1: la TV termina y vuelve el sinusal.']] },
    tvfabl_rf: { t: 'TV fascicular: ablación en P2', lanes: [['His', 'His'], ['LV', 'Septo VI'], ['ECG', 'ECG']], panels: [() => tvfSc('abl')], win: 1600,
      fases: s => [[0, 'TV fascicular posterior. El catéter de ablación (acceso retroaórtico) está sobre el <b>P2 presistólico más precoz</b>, en el fascículo posterior distal (sitio de salida).'], [s[0].rf[0], 'Se aplica <b>RF</b>: el giro inferior se enlentece y P1–P2 se alarga.'], [s[0].stimEnd, 'P1 ya no llega a P2: la TV termina.'], [s[0].stimEnd + 650, 'En sinusal, el fascículo posterior queda bloqueado en el sitio de ablación: P2 aparece tarde.']] },
    conc_gap: { t: 'Reset: la brecha excitable', lanes: [['X', 'Salida'], ['S', 'Sitio de est.'], ['ECG', 'ECG']], panels: [() => loopSc('reset')], win: 1500,
      fases: s => { const t = s[0].m.S[0]; return [[0, 'Circuito de reentrada (LC 340 ms). El frente (naranja) deja detrás tejido refractario; el tramo gris ya se recuperó: es la <b>brecha excitable</b>.'], [t - 120, 'Mirá el sitio de estimulación: el frente ya pasó y el tejido se recuperó.'], [t - 1, 'Se da <b>un extraestímulo</b> en la brecha: sale un frente para cada lado.'], [t + 40, 'El antidrómico (violeta) choca con el frente que venía; el ortodrómico sigue y la salida llega antes.']]; } },
    conc_in: { t: 'Encarrilamiento desde el circuito', lanes: [['X', 'Salida'], ['S', 'Sitio de est.'], ['ECG', 'ECG']], panels: [() => loopSc('in')], win: 1500,
      fases: s => { const S = s[0].m.S; return [[0, 'Circuito de reentrada (LC 340 ms). El sitio de estimulación está en el circuito, en un istmo protegido.'], [S[0] - 10, 'Se estimula a 300 ms: cada estímulo da un frente antidrómico (choca con el anterior) y uno ortodrómico (sigue).'], [S[2], 'La taquicardia se acelera a 300 ms y el QRS no cambia.'], [S[5] + 1, 'Se corta: medí el <b>PPI</b> en el sitio de estimulación.']]; } },
    conc_out: { t: 'Encarrilamiento desde fuera del circuito', lanes: [['X', 'Salida'], ['S', 'Sitio de est.'], ['ECG', 'ECG']], panels: [() => loopSc('out')], win: 1500,
      fases: s => { const S = s[0].m.S; return [[0, 'Circuito de reentrada (LC 340 ms). El sitio de estimulación está fuera, a 60 ms del circuito.'], [S[0] - 10, 'Se estimula a 300 ms: el frente tarda 60 ms en llegar al circuito.'], [S[2], 'La taquicardia se acelera a 300 ms; el QRS tiene <b>fusión constante</b>.'], [S[5] + 1, 'Se corta: medí el <b>PPI</b> en el sitio de estimulación.']]; } },
    vai: { t: 'Índice VA: nodo vs vía posteroseptal', n: 'Índice VA', win: 3900, lanes: [['AD', 'AD alta'], ['His', 'His'], ['VDb', 'VD base'], ['VD', 'VD ápex']], panels: [() => vaiSc('node'), () => vaiSc('ap')],
      fases: s => { const v = s[0].m.va; return [[0, 'Ritmo sinusal, sin inducir la TSV. Un catéter en el ápex del VD y otro en la base posterior, cerca del ostium del SC.'],
        [250, 'Se estimula el <b>ápex</b> sin capturar la aurícula. Medí el VA (espiga → A).'],
        [2250, 'Ahora se estimula la <b>base posterior</b>. Medí el VA.'], [v.base.A + 1, 'Índice VA = VA ápex − VA base.']]; } }
  };
  function entA(def) {
    return { t: 'Encarrilamiento desde el VD: TRAV septal vs TRNAV', n: 'Encarrilamiento desde el VD', def, sel: Object.keys(ENTM).map(k => [k, ENTM[k][0]]),
      panels: k => [() => entr(k, 'trav'), () => entr(k, 'trnav')], fases: (s, k) => entFases(s, ENTM[k][1], ENTM[k][2]) };
  }
  function entFases(s, medir, antes) {
    const sc = s[0], R = sc.m.runs[0], nav = !!sc.nodal;
    const f = [[0, nav ? 'TRNAV típica (LC 340 ms): baja por la vía lenta y sube por la rápida.' : 'TRAV por una vía septal (LC 340 ms): baja por el nodo y sube por la vía.']];
    if (antes) f.push([sc.m.pre[1].v, antes]);
    f.push([R.S[0] - 10, 'Encarrilamiento desde el ápex del VD a 300 ms (E).']);
    if (nav) { const c = R.cap.indexOf(true);
      f.push([R.S[0] + 120, 'Las primeras E no cambian las A: el ventrículo no forma parte del circuito y el frente choca en el His.'],
        [R.S[c] + 100, 'Cuando el estímulo se adelanta lo suficiente, sube por el His hasta el nodo y acelera las A a 300.']); }
    else f.push([R.S[1] + 100, 'El V es parte del circuito: el estímulo sube por la vía y las A se aceleran a 300.']);
    f.push([R.lastS + 1, 'Se corta la estimulación. ' + medir]);
    return f;
  }

  // ---------- Dibujo ----------
  const COL = { ante: '#ef6c00', retro: '#6a3fb5', focus: '#c62828' };
  function drawRing(svg, sc) {
    const T = (x, y, t, o) => { const e = mk('text', Object.assign({ x, y, 'font-size': 14, fill: '#5d1f16' }, o || {}), svg); e.textContent = t; return e; };
    mk('rect', { x: 30, y: 40, width: 500, height: 78, rx: 14, fill: '#f4c7bd', stroke: '#9c4f42', 'stroke-width': 2 }, svg);
    mk('rect', { x: 30, y: 186, width: 500, height: 78, rx: 14, fill: '#e6a091', stroke: '#9c4f42', 'stroke-width': 2 }, svg);
    mk('rect', { x: 30, y: 128, width: 500, height: 48, fill: '#f3e6cc', stroke: '#c9ad7d', 'stroke-width': 1 }, svg);
    T(40, 62, 'aurícula izquierda', { 'font-weight': 700 }); T(40, 256, 'ventrículo izquierdo', { 'font-weight': 700 });
    T(522, 146, 'anillo mitral', { 'font-size': 12, 'text-anchor': 'end', fill: '#7a5a2a' });
    mk('path', { d: 'M18,156 L520,156', stroke: '#5d4037', 'stroke-width': 6, 'stroke-linecap': 'round' }, svg);
    for (const [k, x] of Object.entries(RX)) { mk('rect', { x: x - 7, y: 151, width: 14, height: 10, fill: '#212121' }, svg); T(x, 174, k.slice(1, 2) + '-' + k.slice(2), { 'font-size': 12, 'text-anchor': 'middle', fill: '#212121' }); }
    T(20, 300, '← septal (SC proximal)', { 'font-size': 13, fill: '#455a64' }); T(540, 300, 'lateral (SC distal) →', { 'font-size': 13, fill: '#455a64', 'text-anchor': 'end' });
    mk('path', { d: `M${RAI[0]},${RAI[1]} L${RVI[0]},${RVI[1]}`, stroke: '#d81b60', 'stroke-width': 9, 'stroke-linecap': 'round', opacity: 0.85 }, svg);
    mk('circle', { cx: RAI[0], cy: RAI[1], r: 6, fill: '#d81b60' }, svg); mk('circle', { cx: RVI[0], cy: RVI[1], r: 6, fill: '#d81b60' }, svg);
    T(RAI[0] - 10, 30, 'inserción auricular', { 'font-size': 13, 'font-weight': 700, fill: '#d81b60', 'text-anchor': 'middle' }); mk('path', { d: `M${RAI[0] - 10},34 L${RAI[0]},${RAI[1] - 6}`, stroke: '#d81b60', 'stroke-width': 1.5, 'stroke-dasharray': '3 3' }, svg);
    T(RVI[0], 284, 'inserción ventricular', { 'font-size': 13, 'font-weight': 700, fill: '#d81b60', 'text-anchor': 'middle' }); mk('path', { d: `M${RVI[0]},272 L${RVI[0]},${RVI[1] + 6}`, stroke: '#d81b60', 'stroke-width': 1.5, 'stroke-dasharray': '3 3' }, svg);
    T(345, 146, 'vía oblicua', { 'font-size': 13, 'font-weight': 700, fill: '#d81b60', 'text-anchor': 'end' });
    return { atr: [], ven: [] };
  }
  function drawLoop(svg, sc) {
    const T = (x, y, t, o) => { const e = mk('text', Object.assign({ x, y, 'font-size': 14, fill: '#37474f', stroke: '#fff', 'stroke-width': 4, 'paint-order': 'stroke' }, o || {}), svg); e.textContent = t; return e; };
    mk('circle', { cx: RC[0], cy: RC[1], r: RR, fill: 'none', stroke: '#cfd8dc', 'stroke-width': 20 }, svg);
    mk('circle', { cx: RC[0], cy: RC[1], r: RR - 34, fill: '#eceff1', stroke: '#b0bec5', 'stroke-width': 1.5 }, svg);
    T(RC[0], RC[1] - 4, 'obstáculo', { 'text-anchor': 'middle', fill: '#78909c', 'font-size': 13 });
    T(RC[0], RC[1] + 14, '(cicatriz, anillo)', { 'text-anchor': 'middle', fill: '#90a4ae', 'font-size': 12 });
    const [ex, ey] = sc.loopExit; mk('path', { d: `M${ex},${ey} L${ex + 50},${ey + 46}`, stroke: '#90a4ae', 'stroke-width': 3, 'stroke-dasharray': '5 4' }, svg); T(ex + 56, ey + 60, 'salida al miocardio', { 'font-size': 13 });
    if (sc.loopEntry) { const [sx, sy] = sc.loopSite, [nx, ny] = sc.loopEntry; mk('path', { d: `M${sx},${sy} L${nx},${ny}`, stroke: '#cfd8dc', 'stroke-width': 12, 'stroke-linecap': 'round' }, svg); T(552, sy - 22, 'sitio de estimulación', { 'font-size': 13, 'text-anchor': 'end' }); }
    else { const [sx, sy] = sc.loopSite; T(sx + 22, sy + 5, 'sitio de estimulación', { 'font-size': 13 }); }
    const [qx, qy] = sc.loopSite; mk('circle', { cx: qx, cy: qy, r: 8, fill: '#c62828', stroke: '#fff', 'stroke-width': 2 }, svg);
    mk('path', { d: `M${RC[0] - 20},${RC[1] - RR - 26} L${RC[0] + 20},${RC[1] - RR - 26}`, stroke: '#ef6c00', 'stroke-width': 2.5, 'marker-end': 'url(#ao)' }, svg);
    T(14, 22, 'naranja: refractario (más claro al recuperarse)', { 'font-size': 12, fill: '#546e7a' }); T(14, 38, 'gris: excitable (brecha)', { 'font-size': 12, fill: '#546e7a' });
    const d = mk('defs', {}, svg); d.innerHTML = '<marker id="ao" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ef6c00"/></marker>';
    return { atr: [], ven: [] };
  }
  function drawHeart(svg, sc) {
    if (sc.view === 'ring') return drawRing(svg, sc);
    if (sc.view === 'loop') return drawLoop(svg, sc);
    const g = mk('g', {}, svg); g.innerHTML = HEART;
    const atr = ATR.map(d => mk('path', { d, fill: 'none', opacity: 0 }, svg));
    const ven = VEN.map(d => mk('path', { d, fill: 'none', opacity: 0 }, svg));
    const lbl = (x, y, t, col, anc) => { const e = mk('text', { x, y, 'font-size': 14, 'font-weight': 700, fill: col, 'text-anchor': anc || 'start', stroke: '#fff', 'stroke-width': 4, 'paint-order': 'stroke' }, svg); e.textContent = t; };
    // catéter del VD con el electrodo en el ápex
    // entra por la vena cava inferior a la AD, cruza la tricúspide y baja por dentro del VD hasta el ápex
    const CAT = { apex: 'M18,336 C40,314 62,292 98,270 C140,246 172,258 182,296 C192,360 194,470 182,556',
                  base: 'M18,316 C50,300 90,276 130,268 C180,258 214,270 232,300 C240,314 246,330 250,345',
                  ph: 'M18,316 C60,296 110,272 160,268 C210,264 250,280 278,300',
                  hra: 'M18,336 C50,320 70,280 82,230 C94,180 112,130 140,108',
                  cso: 'M18,336 C70,326 130,312 170,302 C190,297 204,293 215,290',
                  ralat: 'M18,336 C40,320 60,296 72,272 C80,258 86,248 92,238',
                  cs: 'M18,336 C80,322 170,300 215,292 C300,306 420,306 516,290' };
    const CATN = { apex: 'el ápex del VD', base: 'la base del VD', ph: 'la región del His (para-Hisiano)', hra: 'la AD alta', cso: 'el ostium del SC', ralat: 'la pared lateral del AD', cs: 'el seno coronario', abl: 'el VI (acceso retroaórtico)' };
    if (sc.ablPt) { const [x, y] = sc.ablPt; CAT.abl = `M575,96 C560,150 ${x + 70},${y - 140} ${x},${y}`; G.abl = sc.ablPt; }
    const cats = sc.cats || ['apex'];
    cats.forEach(c => { mk('path', { d: CAT[c], stroke: '#fff', 'stroke-width': 9, fill: 'none', 'stroke-linecap': 'round', opacity: 0.7 }, svg);
      mk('path', { d: CAT[c], stroke: c === 'apex' ? '#37474f' : '#5d4037', 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round' }, svg);
      if (c !== 'cs') mk('circle', { cx: G[c][0], cy: G[c][1], r: 8, fill: '#c62828', stroke: '#fff', 'stroke-width': 2 }, svg); });
    if (cats.some(c => c !== 'abl')) mk('text', { x: 18, y: 356, 'font-size': 12, fill: '#37474f' }, svg).textContent = 'VCI';
    mk('text', { x: 52, y: 672, 'font-size': 14, 'font-weight': 700, fill: '#c62828' }, svg).textContent = !cats.length ? '' : cats.length > 1 ? 'catéteres endocavitarios en ' + cats.map(c => CATN[c]).join(' y ') : 'catéter endocavitario en ' + CATN[cats[0]];
    if (sc.nodal) {
      mk('path', { d: 'M266,256 C258,244 246,236 230,234', stroke: '#6a3fb5', 'stroke-width': 4, fill: 'none', 'stroke-dasharray': '6 3', 'stroke-linecap': 'round' }, svg);
      mk('path', { d: 'M228,246 C200,262 208,296 236,288 C250,284 258,276 266,268', stroke: '#ef6c00', 'stroke-width': 4, fill: 'none', 'stroke-dasharray': '6 3', 'stroke-linecap': 'round' }, svg);
      lbl(226, 222, 'vía rápida', '#6a3fb5', 'end'); lbl(200, 312, 'vía lenta', '#ef6c00', 'end');
    }
    if (sc.ap === 'sep') {
      mk('path', { d: 'M231,262 C233,280 235,298 237,318', stroke: '#d81b60', 'stroke-width': 9, fill: 'none', 'stroke-linecap': 'round', opacity: 0.85 }, svg);
      lbl(222, 228, 'vía septal', '#d81b60', 'end');
    } else if (sc.ap === 'nv') {
      mk('path', { d: 'M250,362 C252,332 256,300 264,272', stroke: '#d81b60', 'stroke-width': 8, fill: 'none', 'stroke-linecap': 'round', opacity: 0.85 }, svg);
      lbl(240, 392, 'vía nodoventricular', '#d81b60', 'end');
    } else if (sc.ap === 'af') {
      mk('path', { d: 'M92,272 C80,330 100,430 178,512', stroke: '#d81b60', 'stroke-width': 8, fill: 'none', 'stroke-linecap': 'round', opacity: 0.85 }, svg);
      lbl(58, 520, 'vía', '#d81b60'); lbl(58, 536, 'atriofascicular', '#d81b60');
    } else if (sc.ap && sc.ap !== 'obl') {
      mk('path', { d: 'M519,246 C524,268 530,290 534,322', stroke: '#d81b60', 'stroke-width': 9, fill: 'none', 'stroke-linecap': 'round', opacity: 0.85 }, svg);
      mk('text', { x: 508, y: 238, 'font-size': 15, 'font-weight': 700, fill: '#d81b60', 'text-anchor': 'end' }, svg).textContent = 'vía accesoria';
    }
    if (sc.focus) {
      const FP = sc.focusPt || G.focus, f = mk('g', { transform: `translate(${FP[0]},${FP[1]})` }, svg);
      f.innerHTML = '<path d="M0,-15 L4.5,-4.5 L15,-4.5 L7,2.5 L10,14 L0,7 L-10,14 L-7,2.5 L-15,-4.5 L-4.5,-4.5 Z" fill="#fdd835" stroke="#c62828" stroke-width="2"/>';
      lbl(FP[0] + 20, FP[1] + 5, 'foco', '#c62828');
    }
    if (cats.includes('base')) lbl(G.base[0] - 12, G.base[1] + 4, 'base', '#5d4037', 'end');
    if (cats.includes('cs') && sc.ap === 'obl') for (const [k, [x, y]] of Object.entries(CSX)) { mk('rect', { x: x - 5, y: y - 4, width: 10, height: 8, fill: '#212121' }, svg); mk('text', { x, y: y + 22, 'font-size': 12, 'text-anchor': 'middle', fill: '#212121' }, svg).textContent = k.slice(1, 2) + '-' + k.slice(2); }
    if (sc.ap === 'obl') { mk('path', { d: `M${OBA[0]},${OBA[1]} L${OBV[0]},${OBV[1]}`, stroke: '#d81b60', 'stroke-width': 8, fill: 'none', 'stroke-linecap': 'round', opacity: 0.85 }, svg); lbl(OBA[0] - 6, OBA[1] - 10, 'vía oblicua', '#d81b60', 'end'); }
    if (sc.fasc) { mk('path', { d: `M${P1t[0]},${P1t[1]} L${P1b[0]},${P1b[1]}`, stroke: '#ef6c00', 'stroke-width': 5, 'stroke-dasharray': '7 5', fill: 'none' }, svg);
      lbl(P1m[0] - 10, P1m[1] + 4, 'P1', '#ef6c00', 'end'); lbl(LPFl[0] + 12, LPFl[1] + 2, 'P2', '#6a3fb5'); lbl(LPFb[0] + 6, LPFb[1] + 30, 'fascículo posterior', '#6d4c41');
      mk('path', { d: 'M312,334 C330,400 360,470 400,520', stroke: '#6a3fb5', 'stroke-width': 3, fill: 'none', opacity: 0.45 }, svg); }
    if (sc.rf) { const g = mk('g', { opacity: 0 }, svg); g.innerHTML = `<circle cx="${sc.rf[2][0]}" cy="${sc.rf[2][1]}" r="22" fill="#ff7043" fill-opacity=".45" stroke="#d84315" stroke-width="3"/>`; sc._rfg = g; lbl(sc.rf[2][0] + 26, sc.rf[2][1] + 34, 'RF', '#d84315'); svg.lastChild.setAttribute('opacity', 0); sc._rfl = svg.lastChild; }
    if (sc.twin) { mk('ellipse', { cx: 226, cy: 304, rx: 16, ry: 9, fill: '#f3d36b', stroke: '#9a7300', 'stroke-width': 1.5 }, svg);
      mk('path', { d: 'M232,310 C248,330 264,352 276,376', stroke: '#e2a915', 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round' }, svg);
      lbl(206, 330, 'nodo posterior', '#6d4c41', 'end'); lbl(300, 240, 'nodo anterior', '#6d4c41'); }
    if (!cats.length) mk('text', { x: 18, y: 356, 'font-size': 12, fill: 'transparent' }, svg);
    if (sc.ado) { const g = mk('g', { opacity: 0 }, svg); g.innerHTML = `<circle cx="${G.node[0]}" cy="${G.node[1]}" r="26" fill="#1565c0" fill-opacity=".35" stroke="#1565c0" stroke-width="3"/>`; lbl(G.node[0] + 30, G.node[1] - 24, 'adenosina', '#1565c0'); svg.lastChild.setAttribute('opacity', 0); return { atr, ven, ado: [g, svg.lastChild] }; }
    return { atr, ven };
  }

  const LANES0 = [['AD', 'AD alta'], ['His', 'His'], ['VD', 'VD']];
  const W = 1500, X0 = 46, X1 = 300;        // ventana del trazado (ms) y su ubicación
  function spike(t, y, big, inv) { const h = (big ? 12 : 9) * (inv ? -0.8 : 1); return `M${t - 2} ${y} L${t} ${y - h} L${t + 2} ${y + h * 0.7} L${t + 4} ${y}`; }

  function mount(root) {
    if (root.dataset.on) return; root.dataset.on = 1;
    const A = ANIMS[root.dataset.anim]; if (!A) return;
    const LANES = (A.lanes || LANES0).map(([c, l], i) => [c, l, 46 + i * (A.gap || 41)]), TH = LANES[LANES.length - 1][2] + 26;
    const sel = A.sel ? (root.dataset.sel || A.def) : null;
    const PL = A.sel ? A.panels(sel) : A.panels, scs = (A.pi != null ? [PL[A.pi]] : PL).map(f => f());
    const fases = typeof A.fases === 'function' ? A.fases(scs, sel) : A.fases;
    const dur = A.dur || Math.round(Math.max(...scs.map(s => s.verdictT)) + 650);
    root.innerHTML = `<div class="bl">Animación: ${A.pi != null ? (A.n || A.t) + ' · ' + scs[0].title : A.t}</div>
      <div class="anc"><button class="btn anplay" type="button">▶ Reproducir</button><button class="btn anre" type="button">↺ Reiniciar</button>
      <label class="small">Velocidad <select class="anv"><option value="0.12">muy lenta</option><option value="0.25" selected>lenta</option><option value="0.5">normal</option></select></label>${A.sel ? `<label class="small">${A.selL || 'Medir'} <select class="ansel">${A.sel.map(([k, l]) => `<option value="${k}"${k === sel ? ' selected' : ''}>${l}</option>`).join('')}</select></label>` : ''}</div>
      <input class="ant" type="range" min="0" max="${dur}" value="0" step="10" aria-label="Momento de la animación">
      <p class="anf small"></p>
      <div class="anp"></div>
      <p class="small" style="margin:4px 0 0;opacity:.7">Animación didáctica: tiempos ilustrativos. Naranja: conducción anterógrada · violeta: retrógrada · rojo: foco y estímulo. Las cámaras se iluminan al activarse.</p>`;
    const panels = scs.map(sc => {
      const wrap = document.createElement('div'); wrap.className = 'anpanel';
      wrap.innerHTML = A.pi != null ? '' : `<div class="ant2">${sc.title}</div>`;
      const hsv = mk('svg', { viewBox: sc.vb || VB, role: 'img', 'aria-label': sc.title, class: 'anh' }, wrap);
      const h = drawHeart(hsv, sc);
      const dots = mk('g', {}, hsv);
      const svg = mk('svg', { viewBox: `0 0 310 ${TH}`, role: 'img', 'aria-label': 'Trazado', class: 'antr' }, wrap);
      LANES.forEach(([, lab, y]) => { mk('line', { x1: X0, y1: y, x2: X1, y2: y, stroke: 'var(--line)' }, svg); mk('text', { x: 4, y: y + 4, 'font-size': 10, fill: 'var(--ink2)' }, svg).textContent = lab; });
      const tr = mk('path', { d: '', stroke: 'var(--ink)', 'stroke-width': 1.3, fill: 'none' }, svg);
      const st = mk('path', { d: '', stroke: 'var(--red)', 'stroke-width': 1.6, fill: 'none' }, svg);
      const tg = mk('path', { d: '', stroke: 'var(--blue)', 'stroke-width': 2.2, fill: 'none' }, svg);
      const tp = mk('path', { d: '', stroke: '#d81b60', 'stroke-width': 1.8, fill: 'none' }, svg);
      const ints = mk('g', { 'font-size': 9, 'text-anchor': 'middle' }, svg);
      const lab = mk('g', { 'font-size': 9, fill: 'var(--ink2)', 'text-anchor': 'middle' }, svg);
      const cur = mk('line', { x1: 0, y1: 4, x2: 0, y2: TH - 4, stroke: 'var(--blue)', 'stroke-width': 1 }, svg);
      const ver = document.createElement('div'); ver.className = 'anver'; wrap.appendChild(ver);
      root.querySelector('.anp').appendChild(wrap);
      return { sc, h, tr, st, tg, tp, lab, cur, dots, ver, ints };
    });
    const fas = root.querySelector('.anf'), btn = root.querySelector('.anplay'), rng = root.querySelector('.ant'), vel = root.querySelector('.anv');
    let t = 0, play = false, last = 0;

    function frame(T) {
      for (const p of panels) {
        const { sc } = p;
        // cámaras que se activan
        const lit = (arr, d) => arr.some(x => T >= x && T < x + d);
        const la = lit(sc.flA, 80), lv = lit(sc.flV, 100);
        if (sc.rf) { const on = T >= sc.rf[0] && T < sc.rf[1]; sc._rfg.setAttribute('opacity', on ? 1 : 0); sc._rfl.setAttribute('opacity', on ? 1 : 0); }
        if (p.h.ado) { const on = T >= sc.ado[0] && T < sc.ado[1]; p.h.ado.forEach(x => x.setAttribute('opacity', on ? 1 : 0)); }
        p.h.atr.forEach(e => { e.setAttribute('fill', '#7e57c2'); e.setAttribute('opacity', la ? 0.32 : 0); });
        p.h.ven.forEach(e => { e.setAttribute('fill', '#ff9800'); e.setAttribute('opacity', lv ? 0.3 : 0); });
        // frentes que viajan
        let dh = '';
        for (const w of sc.wv) {
          const t0 = w.pts[0][1], t1 = w.pts[w.pts.length - 1][1];
          if (T < t0 || T > t1 + 40) continue;
          let k = 0; while (k < w.pts.length - 2 && T > w.pts[k + 1][1]) k++;
          const [p0, a0] = w.pts[k], [p1, a1] = w.pts[k + 1];
          const f = Math.max(0, Math.min(1, (T - a0) / Math.max(1, a1 - a0)));
          const x = p0[0] + (p1[0] - p0[0]) * f, y = p0[1] + (p1[1] - p0[1]) * f;
          const trail = w.pts.slice(0, k + 1).map(q => q[0].join(' ')).join(' L') + ` L${x} ${y}`;
          dh += `<path d="M${trail}" stroke="${COL[w.c]}" fill="none" stroke-width="8" stroke-linecap="round" opacity=".55"/><circle cx="${x}" cy="${y}" r="13" fill="${COL[w.c]}" stroke="#fff" stroke-width="3"/>`;
        }
        let df = '';
        for (const f of sc.fronts || []) {
          const dt = T - f.t0; if (dt < 0) continue;
          const maxD = f.dir === 'right' ? 530 - f.x0 : f.dir === 'left' ? f.x0 - 30 : Math.max(f.x0 - 30, 530 - f.x0), tE = maxD * f.k; if (dt > tE + 220) continue;
          const rr = dt / f.k, L = f.dir === 'right' ? f.x0 : Math.max(30, f.x0 - rr), Rr = f.dir === 'left' ? f.x0 : Math.min(530, f.x0 + rr), y = f.band === 'A' ? 40 : 186, col = f.band === 'A' ? '#7e57c2' : '#ef6c00';
          const op = dt < tE ? 0.5 : 0.5 * (1 - (dt - tE) / 220);
          df += `<rect x="${L}" y="${y}" width="${Math.max(0, Rr - L)}" height="78" fill="${col}" opacity="${op.toFixed(2)}"/>`;
          if (dt < tE) { if (Rr < 530 && f.dir !== 'left') df += `<circle cx="${Rr}" cy="${y + 39}" r="10" fill="${col}" stroke="#fff" stroke-width="3"/>`; if (f.dir !== 'right' && L > 30) df += `<circle cx="${L}" cy="${y + 39}" r="10" fill="${col}" stroke="#fff" stroke-width="3"/>`; }
        }
        if (sc.loop) {
          for (let a = 0; a < 360; a += 3) { let last = null; for (const w of sc.loop) { const t = actT(w, a + 1.5, T); if (t != null && (last == null || t > last)) last = t; }
            if (last != null && T - last < RF6) { const [x1, y1] = rpos(a), [x2, y2] = rpos(a + 3.2); df += `<path d="M${x1},${y1} L${x2},${y2}" stroke="#ef6c00" stroke-width="20" opacity="${(0.9 - 0.75 * (T - last) / RF6).toFixed(2)}"/>`; } }
          for (const w of sc.loop) if (T >= w.t0 && T < w.t1 && T - w.t0 < 4000) { const [x, y] = rpos(headA(w, T)); df += `<circle cx="${x}" cy="${y}" r="12" fill="${w.k === 'a' ? '#6a3fb5' : '#ef6c00'}" stroke="#fff" stroke-width="3"/>`; }
          for (const w of sc.loop) if (T >= w.t1 && T < w.t1 + 160) { const [x, y] = rpos(headA(w, w.t1)); df += `<path d="M${x - 11},${y - 11} L${x + 11},${y + 11} M${x + 11},${y - 11} L${x - 11},${y + 11}" stroke="#212121" stroke-width="5" stroke-linecap="round"/>`; }
        }
        dh = df + dh;
        for (const c of sc.cols || []) if (T >= c.t && T < c.t + 140) dh += `<path d="M${c.pt[0] - 11},${c.pt[1] - 11} L${c.pt[0] + 11},${c.pt[1] + 11} M${c.pt[0] + 11},${c.pt[1] - 11} L${c.pt[0] - 11},${c.pt[1] + 11}" stroke="#212121" stroke-width="5" stroke-linecap="round"/>`;
        for (const c of sc.stims || []) if (T >= c.t && T < c.t + 70) dh += `<circle cx="${c.pt[0]}" cy="${c.pt[1]}" r="${c.r || 20}" fill="none" stroke="#c62828" stroke-width="5"/>`;
        for (const n of sc.notes || []) if (T >= n.t0 && T < n.t1) dh += `<text x="${n.x}" y="${n.y}" font-size="15" font-weight="700" fill="${n.col}" text-anchor="${n.anc || 'start'}" stroke="#fff" stroke-width="4" paint-order="stroke">${n.txt}</text>`;
        p.dots.innerHTML = dh;
        // trazado con ventana móvil
        const Wn = A.win || W, tStart = Math.max(0, T - Wn * 0.85), k = (X1 - X0) / Wn, xOf = tt => X0 + (tt - tStart) * k;
        let d = '', ds = '', dt = '', dp = '', lh = '';
        LANES.forEach(([ch, , y]) => { d += `M${X0} ${y} L${xOf(Math.min(T, tStart + Wn))} ${y} `; });
        for (const e of sc.ev) {
          if (e.t > T || e.t < tStart) continue;
          const ln = LANES.find(l => l[0] === e.ch); if (!ln) continue;
          const y = ln[2], x = xOf(e.t);
          if (e.stim) { ds += `M${x} ${y - 16} L${x} ${y + 12} `; lh += `<text x="${x}" y="${y - 18}" style="fill:var(--red)">E</text>`; continue; }
          if (e.l === 'P') { dp += spike(x, y, false); lh += `<text x="${x}" y="${y + 20}" style="fill:#d81b60">P</text>`; continue; }
          if (e.qrs === 'm') { d += `M${x - 1} ${y} L${x + 2} ${y + 9} L${x + 6} ${y - 12} L${x + 9} ${y + 4} L${x + 11} ${y} `; continue; }
          if (e.qrs) { d += e.qrs === 'w' ? `M${x - 1} ${y} L${x + 5} ${y - 12} L${x + 13} ${y - 11} L${x + 19} ${y + 6} L${x + 24} ${y} ` : `M${x - 1} ${y} L${x + 2} ${y - 13} L${x + 5} ${y + 6} L${x + 8} ${y} `; continue; }
          const hot = e.tag && T > (e.tagT || sc.stimEnd);
          if (e.pre && !hot) { d += `M${x - 1} ${y} L${x + 4} ${y - 12} L${x + 10} ${y - 10} L${x + 14} ${y + 6} L${x + 18} ${y} `; lh += `<text x="${x}" y="${y - 14}">${e.l}</text>`; continue; }
          if (hot) dt += spike(x, y, false, e.inv); else d += spike(x, y, e.l === 'V', e.inv);
          lh += `<text x="${x}" y="${y - 14}">${e.l}</text>`;
          if (hot && e.tag.trim()) { const yy = y - (e.tagUp ? 36 : 24); lh += `<text x="${x}" y="${yy}" style="fill:var(--blue)" font-weight="700">${e.tag}</text><line x1="${x}" y1="${yy + 2}" x2="${x}" y2="${y - 22}" style="stroke:var(--blue)"/>`; }
        }
        let di = '';
        for (const it of sc.ints || []) {
          if (T < it.t1 || it.t1 < tStart) continue;
          const ln = LANES.find(l => l[0] === it.ch); if (!ln) continue;
          const up = (it.ch === 'AD' || it.up) && !it.below, y = ln[2] + (up ? -20 : 15), dy = up ? 4 : -4, x0 = Math.max(X0, xOf(it.t0)), x1 = xOf(it.t1), col = it.hot ? 'var(--blue)' : 'var(--ink2)';
          di += `<path d="M${x0} ${y + dy} L${x0} ${y} L${x1} ${y} L${x1} ${y + dy}" fill="none" style="stroke:${col}" stroke-width="1.2"/><text x="${(x0 + x1) / 2}" y="${up ? y - 4 : y + 11}" style="fill:${col}" font-weight="700">${it.l}</text>`;
          if (it.guide) { const g = LANES.find(l => l[0] === it.guide); if (g) di += `<line x1="${x0}" y1="${g[2]}" x2="${x0}" y2="${y}" style="stroke:${col}" stroke-dasharray="2 2"/>`; }
        }
        p.ints.innerHTML = di;
        p.tr.setAttribute('d', d); p.tp.setAttribute('d', dp); p.st.setAttribute('d', ds); p.tg.setAttribute('d', dt); p.lab.innerHTML = lh;
        const xc = xOf(T); p.cur.setAttribute('x1', xc); p.cur.setAttribute('x2', xc);
        p.ver.innerHTML = T >= sc.verdictT ? `<p>${sc.verdict}</p><p class="small" style="margin:0">${sc.why}</p>` : '';
        p.ver.classList.toggle('on', T >= sc.verdictT);
      }
      let txt = ''; for (const [ti, tx] of fases) if (T >= ti) txt = tx;
      fas.innerHTML = txt; rng.value = T;
    }
    function loop(now) {
      if (!play) return;
      const dt = Math.min(100, now - last); last = now;
      t += dt * parseFloat(vel.value);
      if (t >= dur) { t = dur; play = false; btn.textContent = '▶ Reproducir'; }
      frame(t);
      if (play) requestAnimationFrame(loop);
    }
    btn.onclick = () => { play = !play; btn.textContent = play ? '❚❚ Pausa' : '▶ Reproducir'; if (play) { if (t >= dur) t = 0; last = performance.now(); requestAnimationFrame(loop); } };
    const ss = root.querySelector('.ansel');
    if (ss) ss.onchange = () => { play = false; root.dataset.sel = ss.value; delete root.dataset.on; mount(root); };
    root.querySelector('.anre').onclick = () => { t = 0; frame(t); };
    rng.oninput = () => { t = +rng.value; frame(t); };
    frame(0);
  }

  // fichas con varias animaciones, cada una con una sola taquicardia y sus propios controles
  const FOR = { ado: ['ado_trav', 'ado_trnav', 'ado_ta', 'ado_nv', 'ado_jet', 'ado_anti'], basal: ['basal_trnav', 'basal_travl', 'basal_coumel', 'basal_ta'],
    pre: ['pre_dual', 'pre_vanode', 'pre_vaap'], twin: ['twin_tsv', 'twin_ap'], bbr: ['bbr_tv', 'bbr_ppi'], conc: ['conc_gap', 'conc_in', 'conc_out'], tvf: ['tvf_circ', 'tvf_vera'], tvfabl: ['tvfabl_rf'], obl: ['obl_retro', 'obl_ante', 'obl_rev'] };
  for (const k of Object.keys(ANIMS)) {
    const A = ANIMS[k]; if (k.startsWith('ado_')) continue;
    const np = (A.sel ? A.panels(A.def) : A.panels).length; if (np < 2 || FOR[k]) continue;
    FOR[k] = []; for (let i = 0; i < np; i++) { ANIMS[k + '_' + i] = Object.assign({}, A, { pi: i }); FOR[k].push(k + '_' + i); }
  }
  window.ANIM_IDS = Object.keys(ANIMS);
  window.ANIM_FOR = FOR;
  window.mountAnims = r => r.querySelectorAll('.anim[data-anim]').forEach(mount);
})();
