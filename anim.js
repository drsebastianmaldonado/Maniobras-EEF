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
              lvA: [430, 410], lvB: [505, 345], apV: [526, 306], apA: [527, 262], la: [470, 200], focus: [140, 140], ra: [170, 180] };
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

  const ANIMS = {
    vop: { t: 'Sobreestimulación ventricular: A-V vs A-A-V', dur: 4200, panels: [travVop, taVop],
      fases: [[0, 'Taquicardia (LC 340 ms). Mirá el circuito en el esquema y las A, H y V en el trazado.'],
              [690, 'Estimulación del VD a 300 ms (E): cada estímulo llega a la aurícula y las A se aceleran a 300.'],
              [2100, 'Se corta la estimulación. Mirá qué sigue a la <b>última A acelerada</b>.'],
              [3000, 'La taquicardia retoma su ciclo (LC 340) en los dos casos: en la TRAV el frente vuelve a girar por el nodo, el ventrículo y la vía; en la TA vuelve a disparar el foco.']] }
  };

  // ---------- Dibujo ----------
  const COL = { ante: '#ef6c00', retro: '#6a3fb5', focus: '#c62828' };
  function drawHeart(svg, sc) {
    const g = mk('g', {}, svg); g.innerHTML = HEART;
    const atr = ATR.map(d => mk('path', { d, fill: 'none', opacity: 0 }, svg));
    const ven = VEN.map(d => mk('path', { d, fill: 'none', opacity: 0 }, svg));
    if (sc.ap) {
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
    const cat = 'M18,336 C40,314 62,292 98,270 C140,246 172,258 182,296 C192,360 194,470 182,556';
    mk('path', { d: cat, stroke: '#fff', 'stroke-width': 9, fill: 'none', 'stroke-linecap': 'round', opacity: 0.7 }, svg);
    mk('path', { d: cat, stroke: '#37474f', 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round' }, svg);
    mk('text', { x: 18, y: 356, 'font-size': 12, fill: '#37474f' }, svg).textContent = 'VCI';
    mk('circle', { cx: G.apex[0], cy: G.apex[1], r: 8, fill: '#c62828', stroke: '#fff', 'stroke-width': 2 }, svg);
    mk('text', { x: 52, y: 672, 'font-size': 14, 'font-weight': 700, fill: '#c62828' }, svg).textContent = 'catéter endocavitario en el ápex del VD';
    return { atr, ven };
  }

  const LANES = [['AD', 'AD alta', 46], ['His', 'His', 88], ['VD', 'VD', 128]];
  const W = 1500, X0 = 46, X1 = 300;        // ventana del trazado (ms) y su ubicación
  function spike(t, y, big) { const h = big ? 12 : 9; return `M${t - 2} ${y} L${t} ${y - h} L${t + 2} ${y + h * 0.7} L${t + 4} ${y}`; }

  function mount(root) {
    if (root.dataset.on) return; root.dataset.on = 1;
    const A = ANIMS[root.dataset.anim]; if (!A) return;
    root.innerHTML = `<div class="bl">Animación: ${A.t}</div>
      <div class="anc"><button class="btn anplay" type="button">▶ Reproducir</button><button class="btn anre" type="button">↺ Reiniciar</button>
      <label class="small">Velocidad <select class="anv"><option value="0.12">muy lenta</option><option value="0.25" selected>lenta</option><option value="0.5">normal</option></select></label></div>
      <input class="ant" type="range" min="0" max="${A.dur}" value="0" step="10" aria-label="Momento de la animación">
      <p class="anf small"></p>
      <div class="anp"></div>
      <p class="small" style="margin:4px 0 0;opacity:.7">Animación didáctica: tiempos ilustrativos. Naranja: conducción anterógrada · violeta: retrógrada · rojo: foco y estímulo. Las cámaras se iluminan al activarse.</p>`;
    const panels = A.panels.map(f => {
      const sc = f();
      const wrap = document.createElement('div'); wrap.className = 'anpanel';
      wrap.innerHTML = `<div class="ant2">${sc.title}</div>`;
      const hsv = mk('svg', { viewBox: VB, role: 'img', 'aria-label': sc.title, class: 'anh' }, wrap);
      const h = drawHeart(hsv, sc);
      const dots = mk('g', {}, hsv);
      const svg = mk('svg', { viewBox: '0 0 310 142', role: 'img', 'aria-label': 'Trazado', class: 'antr' }, wrap);
      LANES.forEach(([, lab, y]) => { mk('line', { x1: X0, y1: y, x2: X1, y2: y, stroke: 'var(--line)' }, svg); mk('text', { x: 4, y: y + 4, 'font-size': 10, fill: 'var(--ink2)' }, svg).textContent = lab; });
      const tr = mk('path', { d: '', stroke: 'var(--ink)', 'stroke-width': 1.3, fill: 'none' }, svg);
      const st = mk('path', { d: '', stroke: 'var(--red)', 'stroke-width': 1.6, fill: 'none' }, svg);
      const tg = mk('path', { d: '', stroke: 'var(--blue)', 'stroke-width': 2.2, fill: 'none' }, svg);
      const lab = mk('g', { 'font-size': 9, fill: 'var(--ink2)', 'text-anchor': 'middle' }, svg);
      const cur = mk('line', { x1: 0, y1: 4, x2: 0, y2: 138, stroke: 'var(--blue)', 'stroke-width': 1 }, svg);
      const ver = document.createElement('div'); ver.className = 'anver'; wrap.appendChild(ver);
      root.querySelector('.anp').appendChild(wrap);
      return { sc, h, tr, st, tg, lab, cur, dots, ver };
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
        p.dots.innerHTML = dh;
        // trazado con ventana móvil
        const tStart = Math.max(0, T - W * 0.85), k = (X1 - X0) / W, xOf = tt => X0 + (tt - tStart) * k;
        let d = '', ds = '', dt = '', lh = '';
        LANES.forEach(([ch, , y]) => { d += `M${X0} ${y} L${xOf(Math.min(T, tStart + W))} ${y} `; });
        for (const e of sc.ev) {
          if (e.t > T || e.t < tStart) continue;
          const y = LANES.find(l => l[0] === e.ch)[2], x = xOf(e.t);
          if (e.stim) { ds += `M${x} ${y - 16} L${x} ${y + 12} `; lh += `<text x="${x}" y="${y - 18}" style="fill:var(--red)">E</text>`; continue; }
          const hot = e.tag && T > sc.stimEnd;
          if (hot) dt += spike(x, y, false); else d += spike(x, y, e.l === 'V');
          lh += `<text x="${x}" y="${y - 14}">${e.l}</text>`;
          if (hot) { const yy = y - (e.tagUp ? 36 : 24); lh += `<text x="${x}" y="${yy}" style="fill:var(--blue)" font-weight="700">${e.tag}</text><line x1="${x}" y1="${yy + 2}" x2="${x}" y2="${y - 22}" style="stroke:var(--blue)"/>`; }
        }
        p.tr.setAttribute('d', d); p.st.setAttribute('d', ds); p.tg.setAttribute('d', dt); p.lab.innerHTML = lh;
        const xc = xOf(T); p.cur.setAttribute('x1', xc); p.cur.setAttribute('x2', xc);
        p.ver.innerHTML = T >= sc.verdictT ? `<p>${sc.verdict}</p><p class="small" style="margin:0">${sc.why}</p>` : '';
        p.ver.classList.toggle('on', T >= sc.verdictT);
      }
      let txt = ''; for (const [ti, tx] of A.fases) if (T >= ti) txt = tx;
      fas.innerHTML = txt; rng.value = T;
    }
    function loop(now) {
      if (!play) return;
      const dt = Math.min(100, now - last); last = now;
      t += dt * parseFloat(vel.value);
      if (t >= A.dur) { t = A.dur; play = false; btn.textContent = '▶ Reproducir'; }
      frame(t);
      if (play) requestAnimationFrame(loop);
    }
    btn.onclick = () => { play = !play; btn.textContent = play ? '❚❚ Pausa' : '▶ Reproducir'; if (play) { if (t >= A.dur) t = 0; last = performance.now(); requestAnimationFrame(loop); } };
    root.querySelector('.anre').onclick = () => { t = 0; frame(t); };
    rng.oninput = () => { t = +rng.value; frame(t); };
    frame(0);
  }

  window.ANIM_IDS = Object.keys(ANIMS);
  window.mountAnims = r => r.querySelectorAll('.anim[data-anim]').forEach(mount);
})();
