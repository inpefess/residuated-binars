theory T31
imports Main
begin
lemma "(
(\<forall> x::nat. \<forall> y::nat. meet(x, y) = meet(y, x)) &
(\<forall> x::nat. \<forall> y::nat. join(x, y) = join(y, x)) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. meet(x, meet(y, z)) = meet(meet(x, y), z)) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. join(x, join(y, z)) = join(join(x, y), z)) &
(\<forall> x::nat. \<forall> y::nat. meet(x, join(x, y)) = x) &
(\<forall> x::nat. \<forall> y::nat. join(x, meet(x, y)) = x) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. mult(x, join(y, z)) = join(mult(x, y), mult(x, z))) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. mult(join(x, y), z) = join(mult(x, z), mult(y, z))) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. meet(x, over(join(mult(x, y), z), y)) = x) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. meet(y, undr(x, join(mult(x, y), z))) = y) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. join(mult(over(x, y), y), x) = x) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. join(mult(y, undr(y, x)), x) = x) &
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. mult(x, meet(y, z)) = meet(mult(x, y), mult(x, z))) &
(\<forall> x::nat. \<forall> y::nat. invo(join(x, y)) = meet(invo(x), invo(y))) &
(\<forall> x::nat. \<forall> y::nat. invo(meet(x, y)) = join(invo(x), invo(y))) &
(\<forall> x::nat. invo(invo(x)) = x)
) \<longrightarrow>
(\<forall> x::nat. \<forall> y::nat. \<forall> z::nat. mult(meet(x, y), z) = meet(mult(x, z), mult(y, z)))
"
nitpick[card nat=4,timeout=86400]
oops
end