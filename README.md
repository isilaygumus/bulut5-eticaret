Proje Kapsamı ve Amacı

Bu proje, Python framework'ü olan Flask kullanılarak geliştirilen hafif, hızlı ve tek sayfadan oluşan dinamik bir e-ticaret platformu simülasyonudur. Projenin temel amacı, uygulamanın Google Cloud Platform (GCP) üzerinde tam modüler, yüksek erişilebilirliğe sahip ve gelen trafiğe göre otomatik ölçeklenebilir (Auto Scaling) bir mimaride ayağa kaldırılmasıdır.

Başlangıçta yerel (local) ortamda ve geçici hafıza (in-memory) ile simüle edilen proje , nihai aşamada yönetilen bir bulut veritabanına bağlanmış ve trafik yönetimini otonom hale getiren bir bulut mimarisine taşınmıştır.

Kullanılan Teknolojiler

Backend: Python 3.10, Flask.
Veritabanı: Google Cloud SQL (MySQL 8.4).
Arayüz: HTML, Bootstrap (Ana şablon ve tek sayfa mimarisi).
Bulut Altyapısı (GCP): Compute Engine (VM Instances), Global External Application Load Balancer, Managed Instance Groups, Cloud NAT / VPC.

Bulut Mimarisi ve Ölçeklendirme (Autoscaling)
Sistem, gerçek dünya sektör standartlarına uygun olarak bileşenleri ayrılmış (decoupled) bir altyapıya sahiptir:

Yük Dengeleyici (Load Balancer): Dış dünyadan (8.233.255.125 IP adresi üzerinden) gelen HTTP port 80 istekleri Global External Application Load Balancer tarafından karşılanır.
Durum Denetimi (Health Check): Yük dengeleyici, arka plandaki sanal makinelerin (VM) TCP 5000 portuna sürekli istek atarak bulut5-healthcheck kuralı ile sistemin ayakta (Healthy) olup olmadığını denetler.
Yönetilen Örnek Grubu (MIG): Flask kodlarını barındıran e2-micro tipi makineler, bulut5-temiz-sablon kalıbından üretilerek bulut5-grup içinde çalıştırılır.
Otomatik Ölçeklendirme: Ani trafik artışlarında sistem kesintilerini önlemek adına; CPU kullanımı %60'ı geçtiğinde makine sayısı minimum 1'den maksimum 3'e kadar otomatik olarak artırılır.


Dinamik Ağ İzinleri: Ölçeklenen yeni makinelerin IP adresleri değişkenlik göstereceği için, Google Cloud SQL üzerinde 0.0.0.0/0 kuralı ile "Yetkili Ağlar" (Authorized Networks) yapılandırması yapılmış ve bağlantı reddi engellenmiştir.
