theory DistributiveCase
  imports Residuated_Lattices.Residuated_Lattices
begin
  class DistributiveResiduatedBinar=residuated_lgroupoid + distrib_lattice
  begin
  lemma lemma2_2_3:
  "(\<forall> x y z w. (x \<squnion> y) \<rightarrow> (z \<squnion> w) \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w)) \<longleftrightarrow>
    (\<forall> x y z. x \<rightarrow> (y \<squnion> z) = (x \<rightarrow> y) \<squnion> (x \<rightarrow> z))"
    by (metis local.resr_subdist local.resr_superdist_var local.sup_absorb2 local.sup_commute local.sup_idem local.sup_mono)
  lemma lemma2_2_5:
  "(\<forall> x y z w. (x \<sqinter> y) \<rightarrow> (z \<sqinter> w) \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w)) \<longleftrightarrow>
    (\<forall> x y z. (x \<sqinter> y) \<rightarrow> z = (x \<rightarrow> z) \<squnion> (y \<rightarrow> z))"
  proof -
    have "(\<forall> x y z w. (x \<sqinter> y) \<rightarrow> (z \<sqinter> w) \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w)) \<longrightarrow>
    (\<forall> x y z. (x \<sqinter> y) \<rightarrow> z = (x \<rightarrow> z) \<squnion> (y \<rightarrow> z))"
      by (smt (z3) abel_semigroup.commute local.distrib_inf_le local.inf.abel_semigroup_axioms local.inf.orderE local.inf.semilattice_axioms local.resr_distl local.sup_inf_absorb semilattice.idem)
    have "(\<forall> x y z. (x \<sqinter> y) \<rightarrow> z = (x \<rightarrow> z) \<squnion> (y \<rightarrow> z)) \<longrightarrow>
    (\<forall> x y z w. (x \<sqinter> y) \<rightarrow> (z \<sqinter> w) \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w))"
      by (metis local.inf.cobounded1 local.inf.commute local.resr_iso local.sup.mono)
    show ?thesis
      using \<open>(\<forall>x y z w. x \<sqinter> y \<rightarrow> z \<sqinter> w \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w)) \<longrightarrow> (\<forall>x y z. x \<sqinter> y \<rightarrow> z = (x \<rightarrow> z) \<squnion> (y \<rightarrow> z))\<close> \<open>(\<forall>x y z. x \<sqinter> y \<rightarrow> z = (x \<rightarrow> z) \<squnion> (y \<rightarrow> z)) \<longrightarrow> (\<forall>x y z w. x \<sqinter> y \<rightarrow> z \<sqinter> w \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w))\<close> by blast
  qed
  theorem Main:
    assumes one: "\<forall>x y z. (x \<squnion> y) \<leftarrow> z = (x \<leftarrow> z) \<squnion> (y \<leftarrow> z)"
    and two: "\<forall>x y z. (x \<sqinter> y) \<rightarrow> z = (x \<rightarrow> z) \<squnion> (y \<rightarrow> z)"
    shows "\<forall>x y z. x \<rightarrow> (y \<squnion> z) = (x \<rightarrow> y) \<squnion> (x \<rightarrow> z)"
  proof -
    {
      fix x y z w u
      assume "u = (x \<squnion> y) \<rightarrow> (z \<squnion> w)"
      have "u \<le> ((x \<sqinter> (z \<leftarrow> u)) \<rightarrow> z) \<squnion> ((y \<sqinter> (w \<leftarrow> u)) \<rightarrow> w)"
        using local.inf.cobounded2 local.resl_galois local.sup.coboundedI1 by blast
      have "u \<le> ((x \<sqinter> (z \<leftarrow> u)) \<rightarrow> z) \<squnion> ((y \<sqinter> (z \<leftarrow> u)) \<rightarrow> w)"
        using local.inf.cobounded2 local.le_supI1 local.resl_galois by blast
      have "u \<le> ((x \<sqinter> (w \<leftarrow> u)) \<rightarrow> z) \<squnion> ((y \<sqinter> (w \<leftarrow> u)) \<rightarrow> w)"
        using local.inf.cobounded2 local.resl_galois local.sup.coboundedI2 by blast
      have "u \<le> ((x \<sqinter> (w \<leftarrow> u)) \<sqinter> (y \<sqinter> (z \<leftarrow> u))) \<rightarrow> (z \<sqinter> w)"
        by (meson local.inf_le1 local.inf_le2 local.le_inf_iff local.resl_galois local.resrI) 
      have "u \<le> ((x \<sqinter> (w \<leftarrow> u)) \<rightarrow> z) \<squnion> ((y \<sqinter> (z \<leftarrow> u)) \<rightarrow> w)"
        using \<open>u \<le> x \<sqinter> (w \<leftarrow> u) \<sqinter> (y \<sqinter> (z \<leftarrow> u)) \<rightarrow> z \<sqinter> w\<close> lemma2_2_5 local.dual_order.trans two by blast
      have "u \<le>
    (
    (((x \<sqinter> (w \<leftarrow> u)) \<rightarrow> z)
     \<sqinter> ((x \<sqinter> (z \<leftarrow> u))\<rightarrow> z))
     \<squnion> ((y \<sqinter> (z \<leftarrow> u)) \<rightarrow> w)
    ) \<sqinter> (
    (((x \<sqinter> (z \<leftarrow> u)) \<rightarrow> z)
    \<sqinter> ((x \<sqinter> (w \<leftarrow> u)) \<rightarrow> z))
    \<squnion> ((y \<sqinter> (w \<leftarrow> u)) \<rightarrow> w))"
        by (simp add: \<open>u \<le> (x \<sqinter> (w \<leftarrow> u) \<rightarrow> z) \<squnion> (y \<sqinter> (w \<leftarrow> u) \<rightarrow> w)\<close> \<open>u \<le> (x \<sqinter> (w \<leftarrow> u) \<rightarrow> z) \<squnion> (y \<sqinter> (z \<leftarrow> u) \<rightarrow> w)\<close> \<open>u \<le> (x \<sqinter> (z \<leftarrow> u) \<rightarrow> z) \<squnion> (y \<sqinter> (w \<leftarrow> u) \<rightarrow> w)\<close> \<open>u \<le> (x \<sqinter> (z \<leftarrow> u) \<rightarrow> z) \<squnion> (y \<sqinter> (z \<leftarrow> u) \<rightarrow> w)\<close> local.sup_inf_distrib2)
      have "u \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w)"
        by (metis \<open>u = x \<squnion> y \<rightarrow> z \<squnion> w\<close> \<open>u \<le> (x \<sqinter> (w \<leftarrow> u) \<rightarrow> z) \<sqinter> (x \<sqinter> (z \<leftarrow> u) \<rightarrow> z) \<squnion> (y \<sqinter> (z \<leftarrow> u) \<rightarrow> w) \<sqinter> ((x \<sqinter> (z \<leftarrow> u) \<rightarrow> z) \<sqinter> (x \<sqinter> (w \<leftarrow> u) \<rightarrow> z) \<squnion> (y \<sqinter> (w \<leftarrow> u) \<rightarrow> w))\<close> local.inf.order_iff local.inf_sup_distrib1 local.jipsen1l local.le_supE local.resr_distl local.sup.commute local.sup_inf_distrib2 one)
    }
    have "\<forall> x y z w. (x \<squnion> y) \<rightarrow> (z \<squnion> w) \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w)"
      by (simp add: \<open>\<And>z y x w u. u = x \<squnion> y \<rightarrow> z \<squnion> w \<Longrightarrow> u \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w)\<close>)    
    show ?thesis
      using \<open>\<forall>x y z w. x \<squnion> y \<rightarrow> z \<squnion> w \<le> (x \<rightarrow> z) \<squnion> (y \<rightarrow> w)\<close> lemma2_2_3 by blast
    qed
  end
end                                                                                                                  
