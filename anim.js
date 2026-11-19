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
              lvA: [430, 410], lvB: [505, 345], apV: [526, 306], apA: [527, 262], la: [470, 200], focus: [140, 140], ra: [170, 180], base: [250, 345], ph: [278, 300] };
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
  const newSc = o => Object.assign({ ev: [], wv: [], flA: [], flV: [], ints: [], cols: [], stims: [], m: {} }, o);
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

  // PPI−LC, SA−VA y ΔHA: un mismo encarrilamiento con un selector de medición (cada ficha arranca con la suya)
  const ENTM = { ppi: ['PPI − LC', 'Medí el <b>PPI</b> en el canal del VD: de la última espiga al primer V de retorno, y restale la LC.'],
    sava: ['SA − VA', 'Medí el <b>SA</b>: de la última espiga a la A del último latido acelerado, y comparalo con el <b>VA</b> de la TSV.', 'Antes de estimular, mirá el <b>VA</b> de la TSV (del V a la A).'],
    dha: ['ΔHA', 'Medí el <b>HA</b> del último latido estimulado (del His retrógrado a la A) y comparalo con el HA de la TSV.', 'Antes de estimular, mirá el <b>HA</b> de la TSV (del His a la A).'],
    all: ['Las tres', 'Las tres mediciones salen del mismo encarrilamiento: PPI en el canal del VD, SA y VA en la AD alta y HA en el His.', 'Antes de estimular, mirá la LC, el VA y el HA de la TSV.'] };
  const ANIMS = {
    vop: { t: 'Sobreestimulación ventricular: A-V vs A-A-V', dur: 4200, panels: [travVop, taVop],
      fases: [[0, 'Taquicardia (LC 340 ms). Mirá el circuito en el esquema y las A, H y V en el trazado.'],
              [690, 'Estimulación del VD a 300 ms (E): cada estímulo llega a la aurícula y las A se aceleran a 300.'],
              [2100, 'Se corta la estimulación. Mirá qué sigue a la <b>última A acelerada</b>.'],
              [3000, 'La taquicardia retoma su ciclo (LC 340) en los dos casos: en la TRAV el frente vuelve a girar por el nodo, el ventrículo y la vía; en la TA vuelve a disparar el foco.']] },
    ppi: entA('ppi'), sava: entA('sava'), dha: entA('dha'),
    hisorto: { t: 'Captura ortodrómica del His', panels: [() => hisorto(320), () => hisorto(270)],
      fases: s => [[0, 'La misma TRAV, encarrilada desde el ápex del VD a dos LC distintas. Mirá cómo y cuándo se activa el His.'],
        [s[0].m.runs[0].S[0] - 10, 'Estimulación del VD. A la izquierda, a 320 ms (20 ms menos que la LC); a la derecha, a 270 ms.'],
        [s[0].m.runs[0].S[3], 'Seguí el His: a la izquierda baja desde el nodo (naranja) y choca con el estímulo en la rama derecha; a la derecha, el estímulo sube primero por la rama (violeta).'],
        [s[0].stimEnd + 200, 'Al cortar, la taquicardia sigue igual en los dos casos.']] },
    diff: { t: 'Encarrilamiento diferencial: ápex vs base', lanes: [['AD', 'AD alta'], ['His', 'His'], ['VDb', 'VD base'], ['VD', 'VD ápex']], panels: [() => diffSc('trav'), () => diffSc('trnav')],
      fases: s => { const [a, b] = s[0].m.runs; return [[0, 'Taquicardia. Hay un catéter en el ápex del VD y otro en la base, cerca del His.'],
        [a.S[0] - 10, 'Primero se encarrila desde el <b>ápex</b> (a 300 ms).'], [a.lastS + 1, 'Medí el VA (espiga → A) y el PPI desde el ápex.'],
        [b.S[0] - 10, 'Ahora se encarrila desde la <b>base</b>, a la misma LC.'], [b.lastS + 1, 'Medí el VA y el PPI desde la base y restá: base − ápex.']]; } },
    ehr: { t: 'EV con His refractario: TRAV vs TRNAV', dur: 2500, lanes: [['AD', 'AD alta'], ['His', 'His'], ['VDb', 'VD base']], panels: [() => ehrSc('trav'), () => ehrSc('trnav')],
      fases: s => { const e = s[0].stimEnd; return [[0, 'Taquicardia (LC 340 ms). Hay un catéter en la base del VD, cerca de la vía septal.'],
        [e - 60, 'Mirá el His: se activa en forma anterógrada. Desde ese momento el His está refractario.'],
        [e - 4, 'Se da <b>una sola EV</b> desde la base del VD, justo después del His (His refractario). El frente no puede subir por el His.'],
        [e + 110, 'Mirá la A siguiente: ¿llega antes de lo esperado (AA &lt; 340) o a tiempo?'],
        [e + 450, 'Después de la EV la taquicardia sigue. En la TRAV, desde la A adelantada (se reseteó).']]; } },
    parahis: { t: 'Estimulación para-Hisiana: nodo vs vía septal', win: 2600, lanes: [['ECG', 'ECG'], ['AD', 'AD alta'], ['His', 'His']], panels: [() => parahisSc('node'), () => parahisSc('ap')],
      fases: s => { const R = s[0].m.R; return [[0, 'Ritmo sinusal. El catéter está en la región del His.'],
        [R[0].s - 10, '<b>Salida alta</b>: se captura el His y el miocardio vecino. QRS angosto y His inmediato (SH corto).'],
        [R[2].s - 10, '<b>Salida baja</b>: se captura solo el miocardio. QRS ancho (BRI) y aparece el His retrógrado, más tarde (SH largo).'],
        [R[3].s + 1, 'Compará el <b>SA</b> con y sin captura del His (y la secuencia auricular).']]; } },
    vai: { t: 'Índice VA: nodo vs vía posteroseptal', win: 3900, lanes: [['AD', 'AD alta'], ['His', 'His'], ['VDb', 'VD base'], ['VD', 'VD ápex']], panels: [() => vaiSc('node'), () => vaiSc('ap')],
      fases: s => { const v = s[0].m.va; return [[0, 'Ritmo sinusal, sin inducir la TSV. Un catéter en el ápex del VD y otro en la base posterior, cerca del ostium del SC.'],
        [250, 'Se estimula el <b>ápex</b> sin capturar la aurícula. Medí el VA (espiga → A).'],
        [2250, 'Ahora se estimula la <b>base posterior</b>. Medí el VA.'], [v.base.A + 1, 'Índice VA = VA ápex − VA base.']]; } }
  };
  function entA(def) {
    return { t: 'Encarrilamiento desde el VD: TRAV septal vs TRNAV', def, sel: Object.keys(ENTM).map(k => [k, ENTM[k][0]]),
      panels: k => [() => entr(k, 'trav'), () => entr(k, 'trnav')], fases: (s, k) => entFases(s, ENTM[k][1], ENTM[k][2]) };
  }
  function entFases(s, medir, antes) {
    const [tr, nv] = s, R = tr.m.runs[0], N = nv.m.runs[0], c = N.cap.indexOf(true);
    const f = [[0, 'Taquicardia (LC 340 ms). A la izquierda, TRAV por una vía septal; a la derecha, TRNAV típica (baja por la vía lenta y sube por la rápida).']];
    if (antes) f.push([tr.m.pre[1].v, antes]);
    f.push([R.S[0] - 10, 'Encarrilamiento desde el ápex del VD a 300 ms (E).'],
      [N.S[0] + 120, 'En la TRNAV las primeras E no cambian las A: el ventrículo no forma parte del circuito y el frente choca en el His. En la TRAV el V es parte del circuito y las A se aceleran enseguida.'],
      [N.S[c] + 100, 'Cuando el estímulo se adelanta lo suficiente sube por el His hasta el nodo y también acelera las A de la TRNAV (a 300 ms).'],
      [R.lastS + 1, 'Se corta la estimulación. ' + medir]);
    return f;
  }

  // ---------- Dibujo ----------
  const COL = { ante: '#ef6c00', retro: '#6a3fb5', focus: '#c62828' };
  function drawHeart(svg, sc) {
    const g = mk('g', {}, svg); g.innerHTML = HEART;
    const atr = ATR.map(d => mk('path', { d, fill: 'none', opacity: 0 }, svg));
    const ven = VEN.map(d => mk('path', { d, fill: 'none', opacity: 0 }, svg));
    const lbl = (x, y, t, col, anc) => { const e = mk('text', { x, y, 'font-size': 14, 'font-weight': 700, fill: col, 'text-anchor': anc || 'start', stroke: '#fff', 'stroke-width': 4, 'paint-order': 'stroke' }, svg); e.textContent = t; };
    if (sc.nodal) {
      mk('path', { d: 'M266,256 C258,244 246,236 230,234', stroke: '#6a3fb5', 'stroke-width': 4, fill: 'none', 'stroke-dasharray': '6 3', 'stroke-linecap': 'round' }, svg);
      mk('path', { d: 'M228,246 C200,262 208,296 236,288 C250,284 258,276 266,268', stroke: '#ef6c00', 'stroke-width': 4, fill: 'none', 'stroke-dasharray': '6 3', 'stroke-linecap': 'round' }, svg);
      lbl(226, 222, 'vía rápida', '#6a3fb5', 'end'); lbl(200, 312, 'vía lenta', '#ef6c00', 'end');
    }
    if (sc.ap === 'sep') {
      mk('path', { d: 'M231,262 C233,280 235,298 237,318', stroke: '#d81b60', 'stroke-width': 9, fill: 'none', 'stroke-linecap': 'round', opacity: 0.85 }, svg);
      lbl(222, 228, 'vía septal', '#d81b60', 'end');
    } else if (sc.ap) {
      mk('path', { d: 'M519,246 C524,268 530,290 534,322', stroke: '#d81b60', 'stroke-width': 9, fill: 'none', 'stroke-linecap': 'round', opacity: 0.85 }, svg);
      mk('text', { x: 508, y: 238, 'font-size': 15, 'font-weight': 700, fill: '#d81b60', 'text-anchor': 'end' }, svg).textContent = 'vía accesoria';
    }
    if (sc.focus) {
      const f = mk('g', { transform: `translate(${G.focus[0]},${G.focus[1]})` }, svg);
      f.innerHTML = '<path d="M0,-15 L4.5,-4.5 L15,-4.5 L7,2.5 L10,14 L0,7 L-10,14 L-7,2.5 L-15,-4.5 L-4.5,-4.5 Z" fill="#fdd835" stroke="#c62828" stroke-width="2"/>';
      mk('text', { x: G.focus[0] + 20, y: G.focus[1] + 5, 'font-size': 15, 'font-weight': 700, fill: '#c62828' }, svg).textContent = 'foco';
    }
    // catéter del VD con el electrodo en el ápex
    // entra por la vena cava inferior a la AD, cruza la tricúspide y baja por dentro del VD hasta el ápex
    const CAT = { apex: 'M18,336 C40,314 62,292 98,270 C140,246 172,258 182,296 C192,360 194,470 182,556',
                  base: 'M18,316 C50,300 90,276 130,268 C180,258 214,270 232,300 C240,314 246,330 250,345',
                  ph: 'M18,316 C60,296 110,272 160,268 C210,264 250,280 278,300' };
    const cats = sc.cats || ['apex'];
    cats.forEach(c => { mk('path', { d: CAT[c], stroke: '#fff', 'stroke-width': 9, fill: 'none', 'stroke-linecap': 'round', opacity: 0.7 }, svg);
      mk('path', { d: CAT[c], stroke: c === 'apex' ? '#37474f' : '#5d4037', 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round' }, svg);
      mk('circle', { cx: G[c][0], cy: G[c][1], r: 8, fill: '#c62828', stroke: '#fff', 'stroke-width': 2 }, svg); });
    mk('text', { x: 18, y: 356, 'font-size': 12, fill: '#37474f' }, svg).textContent = 'VCI';
    mk('text', { x: 52, y: 672, 'font-size': 14, 'font-weight': 700, fill: '#c62828' }, svg).textContent = cats.length > 1 ? 'catéteres endocavitarios: ápex y base del VD' : cats[0] === 'base' ? 'catéter endocavitario en la base del VD' : cats[0] === 'ph' ? 'catéter para-Hisiano (endocavitario)' : 'catéter endocavitario en el ápex del VD';
    if (cats.includes('base')) lbl(G.base[0] - 12, G.base[1] + 4, 'base', '#5d4037', 'end');
    return { atr, ven };
  }

  const LANES0 = [['AD', 'AD alta'], ['His', 'His'], ['VD', 'VD']];
  const W = 1500, X0 = 46, X1 = 300;        // ventana del trazado (ms) y su ubicación
  function spike(t, y, big, inv) { const h = (big ? 12 : 9) * (inv ? -0.8 : 1); return `M${t - 2} ${y} L${t} ${y - h} L${t + 2} ${y + h * 0.7} L${t + 4} ${y}`; }

  function mount(root) {
    if (root.dataset.on) return; root.dataset.on = 1;
    const A = ANIMS[root.dataset.anim]; if (!A) return;
    const LANES = (A.lanes || LANES0).map(([c, l], i) => [c, l, 46 + i * 41]), TH = LANES[LANES.length - 1][2] + 26;
    const sel = A.sel ? (root.dataset.sel || A.def) : null;
    const scs = (A.sel ? A.panels(sel) : A.panels).map(f => f());
    const fases = typeof A.fases === 'function' ? A.fases(scs, sel) : A.fases;
    const dur = A.dur || Math.round(Math.max(...scs.map(s => s.verdictT)) + 650);
    root.innerHTML = `<div class="bl">Animación: ${A.t}</div>
      <div class="anc"><button class="btn anplay" type="button">▶ Reproducir</button><button class="btn anre" type="button">↺ Reiniciar</button>
      <label class="small">Velocidad <select class="anv"><option value="0.12">muy lenta</option><option value="0.25" selected>lenta</option><option value="0.5">normal</option></select></label>${A.sel ? `<label class="small">Medir <select class="ansel">${A.sel.map(([k, l]) => `<option value="${k}"${k === sel ? ' selected' : ''}>${l}</option>`).join('')}</select></label>` : ''}</div>
      <input class="ant" type="range" min="0" max="${dur}" value="0" step="10" aria-label="Momento de la animación">
      <p class="anf small"></p>
      <div class="anp"></div>
      <p class="small" style="margin:4px 0 0;opacity:.7">Animación didáctica: tiempos ilustrativos. Naranja: conducción anterógrada · violeta: retrógrada · rojo: foco y estímulo. Las cámaras se iluminan al activarse.</p>`;
    const panels = scs.map(sc => {
      const wrap = document.createElement('div'); wrap.className = 'anpanel';
      wrap.innerHTML = `<div class="ant2">${sc.title}</div>`;
      const hsv = mk('svg', { viewBox: VB, role: 'img', 'aria-label': sc.title, class: 'anh' }, wrap);
      const h = drawHeart(hsv, sc);
      const dots = mk('g', {}, hsv);
      const svg = mk('svg', { viewBox: `0 0 310 ${TH}`, role: 'img', 'aria-label': 'Trazado', class: 'antr' }, wrap);
      LANES.forEach(([, lab, y]) => { mk('line', { x1: X0, y1: y, x2: X1, y2: y, stroke: 'var(--line)' }, svg); mk('text', { x: 4, y: y + 4, 'font-size': 10, fill: 'var(--ink2)' }, svg).textContent = lab; });
      const tr = mk('path', { d: '', stroke: 'var(--ink)', 'stroke-width': 1.3, fill: 'none' }, svg);
      const st = mk('path', { d: '', stroke: 'var(--red)', 'stroke-width': 1.6, fill: 'none' }, svg);
      const tg = mk('path', { d: '', stroke: 'var(--blue)', 'stroke-width': 2.2, fill: 'none' }, svg);
      const ints = mk('g', { 'font-size': 9, 'text-anchor': 'middle' }, svg);
      const lab = mk('g', { 'font-size': 9, fill: 'var(--ink2)', 'text-anchor': 'middle' }, svg);
      const cur = mk('line', { x1: 0, y1: 4, x2: 0, y2: TH - 4, stroke: 'var(--blue)', 'stroke-width': 1 }, svg);
      const ver = document.createElement('div'); ver.className = 'anver'; wrap.appendChild(ver);
      root.querySelector('.anp').appendChild(wrap);
      return { sc, h, tr, st, tg, lab, cur, dots, ver, ints };
    });
    const fas = root.querySelector('.anf'), btn = root.querySelector('.anplay'), rng = root.querySelector('.ant'), vel = root.querySelector('.anv');
    let t = 0, play = false, last = 0;

    function frame(T) {
      for (const p of panels) {
        const { sc } = p;
        // cámaras que se activan
        const lit = (arr, d) => arr.some(x => T >= x && T < x + d);
        const la = lit(sc.flA, 80), lv = lit(sc.flV, 100);
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
        for (const c of sc.cols || []) if (T >= c.t && T < c.t + 140) dh += `<path d="M${c.pt[0] - 11},${c.pt[1] - 11} L${c.pt[0] + 11},${c.pt[1] + 11} M${c.pt[0] + 11},${c.pt[1] - 11} L${c.pt[0] - 11},${c.pt[1] + 11}" stroke="#212121" stroke-width="5" stroke-linecap="round"/>`;
        for (const c of sc.stims || []) if (T >= c.t && T < c.t + 70) dh += `<circle cx="${c.pt[0]}" cy="${c.pt[1]}" r="${c.r || 20}" fill="none" stroke="#c62828" stroke-width="5"/>`;
        p.dots.innerHTML = dh;
        // trazado con ventana móvil
        const Wn = A.win || W, tStart = Math.max(0, T - Wn * 0.85), k = (X1 - X0) / Wn, xOf = tt => X0 + (tt - tStart) * k;
        let d = '', ds = '', dt = '', lh = '';
        LANES.forEach(([ch, , y]) => { d += `M${X0} ${y} L${xOf(Math.min(T, tStart + Wn))} ${y} `; });
        for (const e of sc.ev) {
          if (e.t > T || e.t < tStart) continue;
          const ln = LANES.find(l => l[0] === e.ch); if (!ln) continue;
          const y = ln[2], x = xOf(e.t);
          if (e.stim) { ds += `M${x} ${y - 16} L${x} ${y + 12} `; lh += `<text x="${x}" y="${y - 18}" style="fill:var(--red)">E</text>`; continue; }
          if (e.qrs) { d += e.qrs === 'w' ? `M${x - 1} ${y} L${x + 5} ${y - 12} L${x + 13} ${y - 11} L${x + 19} ${y + 6} L${x + 24} ${y} ` : `M${x - 1} ${y} L${x + 2} ${y - 13} L${x + 5} ${y + 6} L${x + 8} ${y} `; continue; }
          const hot = e.tag && T > (e.tagT || sc.stimEnd);
          if (hot) dt += spike(x, y, false, e.inv); else d += spike(x, y, e.l === 'V', e.inv);
          lh += `<text x="${x}" y="${y - 14}">${e.l}</text>`;
          if (hot && e.tag.trim()) { const yy = y - (e.tagUp ? 36 : 24); lh += `<text x="${x}" y="${yy}" style="fill:var(--blue)" font-weight="700">${e.tag}</text><line x1="${x}" y1="${yy + 2}" x2="${x}" y2="${y - 22}" style="stroke:var(--blue)"/>`; }
        }
        let di = '';
        for (const it of sc.ints || []) {
          if (T < it.t1 || it.t1 < tStart) continue;
          const ln = LANES.find(l => l[0] === it.ch); if (!ln) continue;
          const up = it.ch === 'AD' && !it.below, y = ln[2] + (up ? -20 : 15), dy = up ? 4 : -4, x0 = Math.max(X0, xOf(it.t0)), x1 = xOf(it.t1), col = it.hot ? 'var(--blue)' : 'var(--ink2)';
          di += `<path d="M${x0} ${y + dy} L${x0} ${y} L${x1} ${y} L${x1} ${y + dy}" fill="none" style="stroke:${col}" stroke-width="1.2"/><text x="${(x0 + x1) / 2}" y="${up ? y - 4 : y + 11}" style="fill:${col}" font-weight="700">${it.l}</text>`;
          if (it.guide) { const g = LANES.find(l => l[0] === it.guide); if (g) di += `<line x1="${x0}" y1="${g[2]}" x2="${x0}" y2="${y}" style="stroke:${col}" stroke-dasharray="2 2"/>`; }
        }
        p.ints.innerHTML = di;
        p.tr.setAttribute('d', d); p.st.setAttribute('d', ds); p.tg.setAttribute('d', dt); p.lab.innerHTML = lh;
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

  window.ANIM_IDS = Object.keys(ANIMS);
  window.mountAnims = r => r.querySelectorAll('.anim[data-anim]').forEach(mount);
})();
