class Node:
    def __init__(self, id_node, nama, jabatan):
        self.id_node = id_node
        self.nama = nama
        self.jabatan = jabatan
        self.atasan = None
        self.anak = []

    def __str__(self):
        return f"[{self.id_node}] {self.jabatan} - {self.nama}"


class OrganisasiTree:
    def __init__(self):
        self.root = None
        self.jumlah = 0

    # ---------- pencarian berdasarkan ID (iteratif, pakai stack) ----------
    def cari_id(self, id_node):
        if self.root is None:
            return None
        tumpukan = [self.root]
        while len(tumpukan) > 0:
            node = tumpukan.pop()
            if node.id_node == id_node:
                return node
            for a in node.anak:
                tumpukan.append(a)
        return None

    # ---------- a. insert_node ----------
    def insert_node(self, id_atasan, node_baru):
        if self.cari_id(node_baru.id_node) is not None:
            return False                      # ID harus unik
        if self.root is None:
            if id_atasan is not None:
                return False
            self.root = node_baru
            self.jumlah = 1
            return True
        atasan = self.cari_id(id_atasan)
        if atasan is None:
            return False                      # atasan tidak ditemukan
        node_baru.atasan = atasan
        atasan.anak.append(node_baru)
        self.jumlah += 1
        return True

    # ---------- b. search_node (nama atau jabatan) ----------
    def search_node(self, kata):
        kata = kata.lower()
        hasil = []
        if self.root is None:
            return hasil
        tumpukan = [self.root]
        while len(tumpukan) > 0:
            node = tumpukan.pop()
            if kata in node.nama.lower() or kata in node.jabatan.lower():
                hasil.append(node)
            for i in range(len(node.anak) - 1, -1, -1):
                tumpukan.append(node.anak[i])
        return hasil

    # ---------- traversal ----------
    def preorder(self):
        hasil = []
        self._pre(self.root, hasil)
        return hasil

    def _pre(self, node, hasil):
        if node is None:
            return
        hasil.append(node)                    # 1. kunjungi node
        for a in node.anak:                   # 2. lalu semua anak
            self._pre(a, hasil)

    def inorder(self):
        hasil = []
        self._in(self.root, hasil)
        return hasil

    def _in(self, node, hasil):
        if node is None:
            return
        anak = node.anak
        if len(anak) > 0:
            self._in(anak[0], hasil)          # 1. anak pertama
        hasil.append(node)                    # 2. node itu sendiri
        for i in range(1, len(anak)):         # 3. anak-anak sisanya
            self._in(anak[i], hasil)

    def postorder(self):
        hasil = []
        self._post(self.root, hasil)
        return hasil

    def _post(self, node, hasil):
        if node is None:
            return
        for a in node.anak:                   # 1. semua anak dulu
            self._post(a, hasil)
        hasil.append(node)                    # 2. baru node itu sendiri

    # ---------- bantuan: tinggi dan tampilan ----------
    def tinggi(self):
        return self._tinggi(self.root)

    def _tinggi(self, node):
        if node is None:
            return 0
        maks = 0
        for a in node.anak:
            t = self._tinggi(a)
            if t > maks:
                maks = t
        return maks + 1

    def tampilkan(self):
        if self.root is None:
            print("(struktur kosong)")
            return
        print(self.root.jabatan)
        self._cetak(self.root, "")

    def _cetak(self, node, awalan):
        for i in range(len(node.anak)):
            a = node.anak[i]
            terakhir = (i == len(node.anak) - 1)
            print(awalan + ("+-- " if terakhir else "|-- ") + a.jabatan)
            self._cetak(a, awalan + ("    " if terakhir else "|   "))


def buat_struktur_uin():
    data = [
        ("R01", "Pejabat 1", "Rektor", None),
        ("R02", "Pejabat 2", "Senat Universitas", "R01"),
        ("R03", "Pejabat 3", "Wakil Rektor I (Bidang Akademik)", "R01"),
        ("R04", "Pejabat 4", "Wakil Rektor II (Bidang Administrasi Umum & Keuangan)", "R01"),
        ("R05", "Pejabat 5", "Wakil Rektor III (Bidang Kemahasiswaan & Kerja Sama)", "R01"),
        ("D01", "Pejabat 6", "Dekan Fakultas Sains dan Teknologi", "R01"),
        ("D02", "Pejabat 7", "Wakil Dekan I (Bidang Akademik & Kelembagaan)", "D01"),
        ("D03", "Pejabat 8", "Wakil Dekan II (Bidang AUPK)", "D01"),
        ("D04", "Pejabat 9", "Wakil Dekan III (Bidang Kemahasiswaan)", "D01"),
        ("P01", "Pejabat 10", "Ketua Program Studi Teknik Informatika", "D01"),
        ("P02", "Staf 1", "Sekretaris Program Studi", "P01"),
        ("P03", "Dosen 1", "Kepala Laboratorium Komputer", "P01"),
        ("P04", "Staf 2", "Asisten Laboratorium", "P03"),
        ("P05", "Staf 3", "Teknisi Laboratorium", "P03"),
        ("P06", "Dosen 2", "Koordinator Dosen", "P01"),
        ("P07", "Dosen 3", "Dosen Pembimbing Akademik", "P06"),
        ("P08", "Mahasiswa 1", "Mahasiswa Bimbingan", "P07"),
        ("P09", "Dosen 4", "Dosen Pengampu Mata Kuliah", "P06"),
    ]
    tree = OrganisasiTree()
    for id_node, nama, jabatan, atasan in data:
        tree.insert_node(atasan, Node(id_node, nama, jabatan))
    return tree


def cetak_urutan(daftar):
    for i in range(len(daftar)):
        print(f"{i + 1:>2}. {daftar[i].jabatan}")


def menu():
    tree = buat_struktur_uin()
    while True:
        print("\n=== SILSILAH ORGANISASI UIN SUSKA RIAU ===")
        print("1. Tampilkan struktur")
        print("2. Tambah pegawai (insert_node)")
        print("3. Cari pegawai (nama/jabatan)")
        print("4. Preorder")
        print("5. Inorder")
        print("6. Postorder")
        print("7. Info tree (jumlah node dan tinggi)")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            tree.tampilkan()
        elif pilihan == "2":
            id_atasan = input("ID atasan : ").strip()
            id_baru = input("ID baru   : ").strip()
            nama = input("Nama      : ").strip()
            jabatan = input("Jabatan   : ").strip()
            if tree.insert_node(id_atasan, Node(id_baru, nama, jabatan)):
                print("Berhasil ditambahkan.")
            else:
                print("Gagal: ID atasan tidak ada atau ID baru sudah dipakai.")
        elif pilihan == "3":
            hasil = tree.search_node(input("Kata kunci: ").strip())
            if len(hasil) == 0:
                print("Tidak ditemukan.")
            for n in hasil:
                print(n)
        elif pilihan == "4":
            cetak_urutan(tree.preorder())
        elif pilihan == "5":
            cetak_urutan(tree.inorder())
        elif pilihan == "6":
            cetak_urutan(tree.postorder())
        elif pilihan == "7":
            print("Jumlah node:", tree.jumlah)
            print("Tinggi (jumlah tingkat):", tree.tinggi())
        elif pilihan == "0":
            print("Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    menu()