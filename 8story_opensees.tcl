puts "------------------ 8 Story Wall -------------------"
# Create ModelBuilder (with two-dimensions and 3 DOF/node)
wipe
model basic -ndm 2 -ndf 3
file mkdir Output
# Create nodes
# ------------
# Create nodes
#  tag  X    Y 
node 1 0.0 0.0 

node 2   0.0    180 
node 3   0.0		336.0
node 4   0.0		492.0
node 5   0.0		648.0
node 6   0.0		804.0
node 7   0.0		960.0
node 8   0.0		1116.0
node 9   0.0		1272.0
fix 1 1 1 1
# Define materials
# ------------------------------------------
# CONCRETE         tag  fc  ec0  fcu    ecu
uniaxialMaterial Concrete02 11 -6500.0 -0.00282886236782 -650.0   -0.0161417618651 0.1 322.490309932 545542.323764
uniaxialMaterial Concrete02 12 -6500.0 -0.00282886236782  -650.0   -0.00435037864518 0.1 322.490309932 545542.323764
uniaxialMaterial Concrete02 13 -6500.0 -0.00282886236782  -650.0   -0.00372856742069 0.1 322.490309932 545542.323764
uniaxialMaterial Concrete02 21 -6500.0 -0.00282886236782 -650.0   -0.0183639840874 0.1 322.490309932 545542.323764
uniaxialMaterial Concrete02 22 -6500.0 -0.00282886236782  -650.0   -0.00475854191049 0.1 322.490309932 545542.323764
uniaxialMaterial Concrete02 23 -6500.0 -0.00282886236782  -650.0   -0.00404106742069 0.1 322.490309932 545542.323764
uniaxialMaterial Concrete02 31 -10272.0 -0.004  -2054.4   -0.0181159964362 0.1 405.403502698 862124.730724
uniaxialMaterial Concrete02 32 -10272.0 -0.004  -2054.4   -0.00543153532051 0.1 405.403502698 862124.730724
uniaxialMaterial Concrete02 33 -10272.0 -0.004  -2054.4   -0.00476262819136 0.1 405.403502698 862124.730724
uniaxialMaterial Concrete02 41 -10272.0 -0.004  -2054.4   -0.0205065294926 0.1 405.403502698 862124.730724
uniaxialMaterial Concrete02 42 -10272.0 -0.004  -2054.4   -0.00587061282067 0.1 405.403502698 862124.730724
uniaxialMaterial Concrete02 43 -10272.0 -0.004  -2054.4   -0.00509879690242 0.1 405.403502698 862124.730724
uniaxialMaterial SteelMPF  1  70200.0 70200.0 29000000 0.00607351041921 0.00607351041921 20 0.925 0.15 
uniaxialMaterial MinMax   1011  1 -min -0.0161417618651 -max 0.2
uniaxialMaterial MinMax   1012  1 -min -0.00435037864518 -max 0.2
uniaxialMaterial MinMax   1013  1 -min -0.00372856742069 -max 0.2
uniaxialMaterial MinMax   1021  1 -min -0.0183639840874 -max 0.2
uniaxialMaterial MinMax   1022  1 -min -0.00475854191049 -max 0.2
uniaxialMaterial MinMax   1023  1 -min -0.00404106742069 -max 0.2
uniaxialMaterial MinMax   1031  1 -min -0.0181159964362 -max 0.2
uniaxialMaterial MinMax   1032  1 -min -0.00543153532051 -max 0.2
uniaxialMaterial MinMax   1033  1 -min -0.00476262819136 -max 0.2
uniaxialMaterial MinMax   1041  1 -min -0.0205065294926 -max 0.2
uniaxialMaterial MinMax   1042  1 -min -0.00587061282067 -max 0.2
uniaxialMaterial MinMax   1043  1 -min -0.00509879690242 -max 0.2
uniaxialMaterial Steel01 90 50.00 1323500231.96 1.0000
uniaxialMaterial Steel01 91 50.00 6617501159.8 1.0000
set AsBE  1.27
set AsBE1  1.27
set AsWeb  0.2
section Fiber 1 {
patch rect 31 72 1 -177.0  -9.0 -108.0 9.0
patch rect 31 72 1 108.0 -9.0 177.0   9.0
patch rect 11 360 1 -180.0 9.0 180.0 12.0
patch rect 11 360 1 -180.0 -12.0 180.0 -9.0
patch rect 11 1 1 -180.0 -9.0 -177.0 9.0
patch rect 11 1 1 177.0 -9.0 180.0 9.0
patch rect 11 216 1 -108.0 -9.0 108.0 9.0
layer straight 1031 16 $AsBE 108.0 9.0 177.0 9.0
layer straight 1031 16 $AsBE 108.0 -9.0 177.0 -9.0
layer straight 1031 16 $AsBE -177.0 9.0 -108.0 9.0
layer straight 1031 16 $AsBE -177.0 -9.0 -108.0 -9.0
layer straight 1031 2 $AsBE 108.0 0 177.0 0
layer straight 1031 2 $AsBE -177.0 0 -108.0 0
layer straight 1011 33 $AsWeb -102.0 9.0 102.0 9.0
layer straight 1011 33 $AsWeb -102.0 -9.0 102.0 -9.0
}  
section Fiber 2 {
patch rect 32 72 1 -177.0  -9.0 -108.0 9.0
patch rect 32 72 1 108.0 -9.0 177.0   9.0
patch rect 12 360 1 -180.0      9.0 180.0         12.0
patch rect 12 360 1 -180.0      -12.0    180.0         -9.0
patch rect 12 1 1 -180.0      -9.0 -177.0  9.0
patch rect 12 1 1 177.0   -9.0 180.0         9.0
patch rect 12 216 1 -108.0 -9.0 108.0 9.0
layer straight 1032 16 $AsBE 108.0 9.0 177.0 9.0
layer straight 1032 16 $AsBE 108.0 -9.0 177.0 -9.0
layer straight 1032 16 $AsBE -177.0 9.0 -108.0 9.0
layer straight 1032 16 $AsBE -177.0 -9.0 -108.0 -9.0
layer straight 1032 2 $AsBE 108.0 0 177.0 0
layer straight 1032 2 $AsBE -177.0 0 -108.0 0
layer straight 1012 33 $AsWeb -102.0 9.0 102.0 9.0
layer straight 1012 33 $AsWeb -102.0 -9.0 102.0 -9.0
} 
section Fiber 3 {
patch rect 33 72 1 -177.0  -9.0 -108.0 9.0
patch rect 33 72 1 108.0 -9.0 177.0   9.0
patch rect 13 360 1 -180.0      9.0 180.0         12.0
patch rect 13 360 1 -180.0      -12.0    180.0         -9.0
patch rect 13 1  1 -180.0      -9.0 -177.0  9.0
patch rect 13 1 1 177.0   -9.0 180.0         9.0
patch rect 13 216 1 -108.0 -9.0 108.0 9.0
layer straight 1033 16 $AsBE 108.0 9.0 177.0 9.0
layer straight 1033 16 $AsBE 108.0 -9.0 177.0 -9.0
layer straight 1033 16 $AsBE -177.0 9.0 -108.0 9.0
layer straight 1033 16 $AsBE -177.0 -9.0 -108.0 -9.0
layer straight 1033 2 $AsBE 108.0 0 177.0 0
layer straight 1033 2 $AsBE -177.0 0 -108.0 0
layer straight 1013 33 $AsWeb -102.0 9.0 102.0 9.0
layer straight 1013 33 $AsWeb -102.0 -9.0 102.0 -9.0
} 
section Fiber 4 {
patch rect 41 72 1 -177.0  -9.0 -108.0 9.0
patch rect 41 72 1 108.0 -9.0 177.0   9.0
patch rect 21 360 1 -180.0      9.0 180.0         12.0
patch rect 21 360 1 -180.0      -12.0    180.0         -9.0
patch rect 21 1  1 -180.0      -9.0 -177.0  9.0
patch rect 21 1  1 177.0   -9.0 180.0         9.0
patch rect 21 216 1 -108.0 -9.0 108.0 9.0
layer straight 1041 16 $AsBE 108.0 9.0 177.0 9.0
layer straight 1041 16 $AsBE 108.0 -9.0 177.0 -9.0
layer straight 1041 16 $AsBE -177.0 9.0 -108.0 9.0
layer straight 1041 16 $AsBE -177.0 -9.0 -108.0 -9.0
layer straight 1041 2 $AsBE 108.0 0 177.0 0
layer straight 1041 2 $AsBE -177.0 0 -108.0 0
layer straight 1021 33 $AsWeb -102.0 9.0 102.0 9.0
layer straight 1021 33 $AsWeb -102.0 -9.0 102.0 -9.0
}  
section Fiber 5 {
patch rect 42 72 1 -177.0  -9.0 -108.0 9.0
patch rect 42 72 1 108.0 -9.0 177.0   9.0
patch rect 22 360 1 -180.0      9.0 180.0         12.0
patch rect 22 360 1 -180.0      -12.0    180.0         -9.0
patch rect 22 1  1 -180.0      -9.0 -177.0  9.0
patch rect 22 1  1 177.0   -9.0 180.0         9.0
patch rect 22 216 1 -108.0 -9.0 108.0 9.0
layer straight 1042 16 $AsBE 108.0 9.0 177.0 9.0
layer straight 1042 16 $AsBE 108.0 -9.0 177.0 -9.0
layer straight 1042 16 $AsBE -177.0 9.0 -108.0 9.0
layer straight 1042 16 $AsBE -177.0 -9.0 -108.0 -9.0
layer straight 1042 2 $AsBE 108.0 0 177.0 0
layer straight 1042 2 $AsBE -177.0 0 -108.0 0
layer straight 1022 33 $AsWeb -102.0 9.0 102.0 9.0
layer straight 1022 33 $AsWeb -102.0 -9.0 102.0 -9.0
}
section Fiber 6 {
patch rect 43 72 1 -177.0  -9.0 -108.0 9.0
patch rect 43 72 1 108.0 -9.0 177.0   9.0
patch rect 23 360 1 -180.0      9.0 180.0         12.0
patch rect 23 360 1 -180.0      -12.0    180.0         -9.0
patch rect 23 1  1 -180.0      -9.0 -177.0  9.0
patch rect 23 1  1 177.0   -9.0 180.0         9.0
patch rect 23 216 1 -108.0 -9.0 108.0 9.0
layer straight 1043 16 $AsBE 108.0 9.0 177.0 9.0
layer straight 1043 16 $AsBE 108.0 -9.0 177.0 -9.0
layer straight 1043 16 $AsBE -177.0 9.0 -108.0 9.0
layer straight 1043 16 $AsBE -177.0 -9.0 -108.0 -9.0
layer straight 1043 2 $AsBE 108.0 0 177.0 0
layer straight 1043 2 $AsBE -177.0 0 -108.0 0
layer straight 1023 33 $AsWeb -102.0 9.0 102.0 9.0
layer straight 1023 33 $AsWeb -102.0 -9.0 102.0 -9.0
}
section Fiber 7 {
patch rect 41 36 1 -177.0  -9.0 -144.0 9.0
patch rect 41 36 1 144.0 -9.0 177.0   9.0
patch rect 21 360 1 -180.0      9.0 180.0         12.0
patch rect 21 360 1 -180.0      -12.0    180.0         -9.0
patch rect 21 1  1 -180.0      -9.0 -177.0  9.0
patch rect 21 1  1 177.0   -9.0 180.0         9.0
patch rect 21 288 1 -144.0 -9.0 144.0 9.0
layer straight 1041 8 $AsBE1 144.0 9.0 177.0 9.0
layer straight 1041 8 $AsBE1 144.0 -9.0 177.0 -9.0
layer straight 1041 8 $AsBE1 -177.0 9.0 -144.0 9.0
layer straight 1041 8 $AsBE1 -177.0 -9.0 -144.0 -9.0
layer straight 1041 2 $AsBE 144.0 0 177.0 0
layer straight 1041 2 $AsBE -177.0 0 -144.0 0
layer straight 1021 44 $AsWeb -138.0 9.0 138.0 9.0
layer straight 1021 44 $AsWeb -138.0 -9.0 138.0 -9.0
}  
section Fiber 8 {
patch rect 42 36 1 -177.0  -9.0 -144.0 9.0
patch rect 42 36 1 144.0 -9.0 177.0   9.0
patch rect 22 360 1 -180.0      9.0 180.0         12.0
patch rect 22 360 1 -180.0      -12.0    180.0         -9.0
patch rect 22 1  1 -180.0      -9.0 -177.0  9.0
patch rect 22 1  1 177.0   -9.0 180.0         9.0
patch rect 22 288 1 -144.0 -9.0 144.0 9.0
layer straight 1042 8 $AsBE1 144.0 9.0 177.0 9.0
layer straight 1042 8 $AsBE1 144.0 -9.0 177.0 -9.0
layer straight 1042 8 $AsBE1 -177.0 9.0 -144.0 9.0
layer straight 1042 8 $AsBE1 -177.0 -9.0 -144.0 -9.0
layer straight 1042 2 $AsBE 144.0 0 177.0 0
layer straight 1042 2 $AsBE -177.0 0 -144.0 0
layer straight 1022 44 $AsWeb -138.0 9.0 138.0 9.0
layer straight 1022 44 $AsWeb -138.0 -9.0 138.0 -9.0
}
section Fiber 9 {
patch rect 43 36 1 -177.0  -9.0 -144.0 9.0
patch rect 43 36 1 144.0 -9.0 177.0   9.0
patch rect 23 360 1 -180.0      9.0 180.0         12.0
patch rect 23 360 1 -180.0      -12.0    180.0         -9.0
patch rect 23 1  1 -180.0      -9.0 -177.0  9.0
patch rect 23 1  1 177.0   -9.0 180.0         9.0
patch rect 23 288 1 -144.0 -9.0 144.0 9.0
layer straight 1043 8 $AsBE1 144.0 9.0 177.0 9.0
layer straight 1043 8 $AsBE1 144.0 -9.0 177.0 -9.0
layer straight 1043 8 $AsBE1 -177.0 9.0 -144.0 9.0
layer straight 1043 8 $AsBE1 -177.0 -9.0 -144.0 -9.0
layer straight 1043 2 $AsBE 144.0 0 177.0 0
layer straight 1043 2 $AsBE -177.0 0 -144.0 0
layer straight 1023 44 $AsWeb -138.0 9.0 138.0 9.0
layer straight 1023 44 $AsWeb -138.0 -9.0 138.0 -9.0
}
section Fiber 10 {
patch rect 21 360 1 -180.0 -12.0 180.0 12.0
layer straight 1021 55 $AsWeb -177.0 9.0 177.0 9.0
layer straight 1021 55 $AsWeb -177.0 -9.0 177.0 -9.0
}  
section Fiber 11 {
patch rect 22 360 1 -180.0 -12.0 180.0 12.0
layer straight 1022 55 $AsWeb -177.0 9.0 177.0 9.0
layer straight 1022 55 $AsWeb -177.0 -9.0 177.0 -9.0
}
section Fiber 12 {
patch rect 23 360 1 -180.0 -12.0 180.0 12.0
layer straight 1023 55 $AsWeb -177.0 9.0 177.0 9.0
layer straight 1023 55 $AsWeb -177.0 -9.0 177.0 -9.0
}
geomTransf Corotational 1
section Aggregator 101 90 Vy -section 1
section Aggregator 102 90 Vy -section 2
section Aggregator 103 90 Vy -section 3
section Aggregator 104 91 Vy -section 4
section Aggregator 105 91 Vy -section 5
section Aggregator 106 91 Vy -section 6
section Aggregator 107 91 Vy -section 7
section Aggregator 108 91 Vy -section 8
section Aggregator 109 91 Vy -section 9
section Aggregator 1010 91 Vy -section 10
section Aggregator 1011 91 Vy -section 11
section Aggregator 1012 91 Vy -section 12
set locations {0.0 0.172673165 0.5 0.827326835 1.0}
set weights  {0.05 0.27222222 0.3555555555 0.27222222 0.05}
set secTags1  {101 102 103 102 101}
set secTags2  {104 105 106 105 104}
set secTags3  {107 108 109 108 107}
set secTags4  {1010 1011 1012 1011 1010}
set elemTol 1e-06 
element forceBeamColumn 1 1 2 1 UserDefined 5 $secTags1 $locations $weights -iter 10 $elemTol
element forceBeamColumn 2 2 3 1 UserDefined 5 $secTags2 $locations $weights -iter 10 $elemTol
element forceBeamColumn 3 3 4 1 UserDefined 5 $secTags3 $locations $weights -iter 10 $elemTol
element forceBeamColumn 4 4 5 1 UserDefined 5 $secTags3 $locations $weights -iter 10 $elemTol
element forceBeamColumn 5 5 6 1 UserDefined 5 $secTags3 $locations $weights -iter 10 $elemTol
element forceBeamColumn 6 6 7 1 UserDefined 5 $secTags4 $locations $weights -iter 10 $elemTol
element forceBeamColumn 7 7 8 1 UserDefined 5 $secTags4 $locations $weights -iter 10 $elemTol
element forceBeamColumn 8 8 9 1 UserDefined 5 $secTags4 $locations $weights -iter 10 $elemTol
recorder Element -file Output/story1_SS_EC_Comp1.txt -time -ele 1 section 1 fiber -180.0 0.0 11 stressStrain
recorder Element -file Output/story1_SS_CC_Comp1.txt -time -ele 1 section 1 fiber -176.0 0.0 31 stressStrain
recorder Element -file Output/story1_SS_ES_Comp1.txt -time -ele 1 section 1 fiber -177.0 9.0 1031 stressStrain
recorder Element -file Output/story1_SS_EC_Ten1.txt -time -ele 1 section 1 fiber 180.0 0.0 11 stressStrain
recorder Element -file Output/story1_SS_CC_Ten1.txt -time -ele 1 section 1 fiber 176.0 0.0 31 stressStrain
recorder Element -file Output/story1_SS_ES_Ten1.txt -time -ele 1 section 1 fiber 177.0 9.0 1031 stressStrain
recorder Element -file Output/story2_SS_EC_Comp1.txt -time -ele 2 section 1 fiber -180.0 0.0 21 stressStrain
recorder Element -file Output/story2_SS_CC_Comp1.txt -time -ele 2 section 1 fiber -176.0 0.0 41 stressStrain
recorder Element -file Output/story2_SS_ES_Comp1.txt -time -ele 2 section 1 fiber -177.0 9.0 1041 stressStrain
recorder Element -file Output/story2_SS_EC_Ten1.txt -time -ele 2 section 1 fiber 180.0 0.0 21 stressStrain
recorder Element -file Output/story2_SS_CC_Ten1.txt -time -ele 2 section 1 fiber 176.0 0.0 41 stressStrain
recorder Element -file Output/story2_SS_ES_Ten1.txt -time -ele 2 section 1 fiber 177.0 9.0 1041 stressStrain
recorder Element -file Output/story3_SS_EC_Comp1.txt -time -ele 3 section 1 fiber -180.0 0.0 21 stressStrain
recorder Element -file Output/story3_SS_CC_Comp1.txt -time -ele 3 section 1 fiber -176.0 0.0 41 stressStrain
recorder Element -file Output/story3_SS_ES_Comp1.txt -time -ele 3 section 1 fiber -177.0 9.0 1041 stressStrain
recorder Element -file Output/story3_SS_EC_Ten1.txt -time -ele 3 section 1 fiber 180.0 0.0 21 stressStrain
recorder Element -file Output/story3_SS_CC_Ten1.txt -time -ele 3 section 1 fiber 176.0 0.0 41 stressStrain
recorder Element -file Output/story3_SS_ES_Ten1.txt -time -ele 3 section 1 fiber 177.0 9.0 1041 stressStrain
recorder Element -file Output/story4_SS_EC_Comp1.txt -time -ele 4 section 1 fiber -180.0 0.0 21 stressStrain
recorder Element -file Output/story4_SS_CC_Comp1.txt -time -ele 4 section 1 fiber -176.0 0.0 41 stressStrain
recorder Element -file Output/story4_SS_ES_Comp1.txt -time -ele 4 section 1 fiber -177.0 9.0 1041 stressStrain
recorder Element -file Output/story4_SS_EC_Ten1.txt -time -ele 4 section 1 fiber 180.0 0.0 21 stressStrain
recorder Element -file Output/story4_SS_CC_Ten1.txt -time -ele 4 section 1 fiber 176.0 0.0 41 stressStrain
recorder Element -file Output/story4_SS_ES_Ten1.txt -time -ele 4 section 1 fiber 177.0 9.0 1041 stressStrain
recorder Element -file Output/story5_SS_EC_Comp1.txt -time -ele 5 section 1 fiber -180.0 0.0 21 stressStrain
recorder Element -file Output/story5_SS_CC_Comp1.txt -time -ele 5 section 1 fiber -176.0 0.0 41 stressStrain
recorder Element -file Output/story5_SS_ES_Comp1.txt -time -ele 5 section 1 fiber -177.0 9.0 1041 stressStrain
recorder Element -file Output/story5_SS_EC_Ten1.txt -time -ele 5 section 1 fiber 180.0 0.0 21 stressStrain
recorder Element -file Output/story5_SS_CC_Ten1.txt -time -ele 5 section 1 fiber 176.0 0.0 41 stressStrain
recorder Element -file Output/story5_SS_ES_Ten1.txt -time -ele 5 section 1 fiber 177.0 9.0 1041 stressStrain
recorder Element -file Output/story6_SS_EC_Comp1.txt -time -ele 6 section 1 fiber -180.0 0.0 21 stressStrain
recorder Element -file Output/story6_SS_ES_Comp1.txt -time -ele 6 section 1 fiber -177.0 9.0 1021 stressStrain
recorder Element -file Output/story6_SS_EC_Ten1.txt -time -ele 6 section 1 fiber 180.0 0.0 21 stressStrain
recorder Element -file Output/story6_SS_ES_Ten1.txt -time -ele 6 section 1 fiber 177.0 9.0 1021 stressStrain
recorder Element -file Output/story7_SS_EC_Comp1.txt -time -ele 7 section 1 fiber -180.0 0.0 21 stressStrain
recorder Element -file Output/story7_SS_ES_Comp1.txt -time -ele 7 section 1 fiber -177.0 9.0 1021 stressStrain
recorder Element -file Output/story7_SS_EC_Ten1.txt -time -ele 7 section 1 fiber 180.0 0.0 21 stressStrain
recorder Element -file Output/story7_SS_ES_Ten1.txt -time -ele 7 section 1 fiber 177.0 9.0 1021 stressStrain
recorder Element -file Output/story8_SS_EC_Comp1.txt -time -ele 8 section 1 fiber -180.0 0.0 21 stressStrain
recorder Element -file Output/story8_SS_ES_Comp1.txt -time -ele 8 section 1 fiber -177.0 9.0 1021 stressStrain
recorder Element -file Output/story8_SS_EC_Ten1.txt -time -ele 8 section 1 fiber 180.0 0.0 21 stressStrain
recorder Element -file Output/story8_SS_ES_Ten1.txt -time -ele 8 section 1 fiber 177.0 9.0 1021 stressStrain
recorder Element -file Output/story1_SS_EC_Comp2.txt -time -ele 1 section 2 fiber -180.0 0.0 12 stressStrain
recorder Element -file Output/story1_SS_CC_Comp2.txt -time -ele 1 section 2 fiber -176.0 0.0 32 stressStrain
recorder Element -file Output/story1_SS_ES_Comp2.txt -time -ele 1 section 2 fiber -177.0 9.0 1032 stressStrain
recorder Element -file Output/story1_SS_EC_Ten2.txt -time -ele 1 section 2 fiber 180.0 0.0 12 stressStrain
recorder Element -file Output/story1_SS_CC_Ten2.txt -time -ele 1 section 2 fiber 176.0 0.0 32 stressStrain
recorder Element -file Output/story1_SS_ES_Ten2.txt -time -ele 1 section 2 fiber 177.0 9.0 1032 stressStrain
recorder Element -file Output/story2_SS_EC_Comp2.txt -time -ele 2 section 2 fiber -180.0 0.0 22 stressStrain
recorder Element -file Output/story2_SS_CC_Comp2.txt -time -ele 2 section 2 fiber -176.0 0.0 42 stressStrain
recorder Element -file Output/story2_SS_ES_Comp2.txt -time -ele 2 section 2 fiber -177.0 9.0 1042 stressStrain
recorder Element -file Output/story2_SS_EC_Ten2.txt -time -ele 2 section 2 fiber 180.0 0.0 22 stressStrain
recorder Element -file Output/story2_SS_CC_Ten2.txt -time -ele 2 section 2 fiber 176.0 0.0 42 stressStrain
recorder Element -file Output/story2_SS_ES_Ten2.txt -time -ele 2 section 2 fiber 177.0 9.0 1042 stressStrain
recorder Element -file Output/story3_SS_EC_Comp2.txt -time -ele 3 section 2 fiber -180.0 0.0 22 stressStrain
recorder Element -file Output/story3_SS_CC_Comp2.txt -time -ele 3 section 2 fiber -176.0 0.0 42 stressStrain
recorder Element -file Output/story3_SS_ES_Comp2.txt -time -ele 3 section 2 fiber -177.0 9.0 1042 stressStrain
recorder Element -file Output/story3_SS_EC_Ten2.txt -time -ele 3 section 2 fiber 180.0 0.0 22 stressStrain
recorder Element -file Output/story3_SS_CC_Ten2.txt -time -ele 3 section 2 fiber 176.0 0.0 42 stressStrain
recorder Element -file Output/story3_SS_ES_Ten2.txt -time -ele 3 section 2 fiber 177.0 9.0 1042 stressStrain
recorder Element -file Output/story4_SS_EC_Comp2.txt -time -ele 4 section 2 fiber -180.0 0.0 22 stressStrain
recorder Element -file Output/story4_SS_CC_Comp2.txt -time -ele 4 section 2 fiber -176.0 0.0 42 stressStrain
recorder Element -file Output/story4_SS_ES_Comp2.txt -time -ele 4 section 2 fiber -177.0 9.0 1042 stressStrain
recorder Element -file Output/story4_SS_EC_Ten2.txt -time -ele 4 section 2 fiber 180.0 0.0 22 stressStrain
recorder Element -file Output/story4_SS_CC_Ten2.txt -time -ele 4 section 2 fiber 176.0 0.0 42 stressStrain
recorder Element -file Output/story4_SS_ES_Ten2.txt -time -ele 4 section 2 fiber 177.0 9.0 1042 stressStrain
recorder Element -file Output/story5_SS_EC_Comp2.txt -time -ele 5 section 2 fiber -180.0 0.0 22 stressStrain
recorder Element -file Output/story5_SS_CC_Comp2.txt -time -ele 5 section 2 fiber -176.0 0.0 42 stressStrain
recorder Element -file Output/story5_SS_ES_Comp2.txt -time -ele 5 section 2 fiber -177.0 9.0 1042 stressStrain
recorder Element -file Output/story5_SS_EC_Ten2.txt -time -ele 5 section 2 fiber 180.0 0.0 22 stressStrain
recorder Element -file Output/story5_SS_CC_Ten2.txt -time -ele 5 section 2 fiber 176.0 0.0 42 stressStrain
recorder Element -file Output/story5_SS_ES_Ten2.txt -time -ele 5 section 2 fiber 177.0 9.0 1042 stressStrain
recorder Element -file Output/story6_SS_EC_Comp2.txt -time -ele 6 section 2 fiber -180.0 0.0 22 stressStrain
recorder Element -file Output/story6_SS_ES_Comp2.txt -time -ele 6 section 2 fiber -177.0 9.0 1022 stressStrain
recorder Element -file Output/story6_SS_EC_Ten2.txt -time -ele 6 section 2 fiber 180.0 0.0 22 stressStrain
recorder Element -file Output/story6_SS_ES_Ten2.txt -time -ele 6 section 2 fiber 177.0 9.0 1022 stressStrain
recorder Element -file Output/story7_SS_EC_Comp2.txt -time -ele 7 section 2 fiber -180.0 0.0 22 stressStrain
recorder Element -file Output/story7_SS_ES_Comp2.txt -time -ele 7 section 2 fiber -177.0 9.0 1022 stressStrain
recorder Element -file Output/story7_SS_EC_Ten2.txt -time -ele 7 section 2 fiber 180.0 0.0 22 stressStrain
recorder Element -file Output/story7_SS_ES_Ten2.txt -time -ele 7 section 2 fiber 177.0 9.0 1022 stressStrain
recorder Element -file Output/story8_SS_EC_Comp2.txt -time -ele 8 section 2 fiber -180.0 0.0 22 stressStrain
recorder Element -file Output/story8_SS_ES_Comp2.txt -time -ele 8 section 2 fiber -177.0 9.0 1022 stressStrain
recorder Element -file Output/story8_SS_EC_Ten2.txt -time -ele 8 section 2 fiber 180.0 0.0 22 stressStrain
recorder Element -file Output/story8_SS_ES_Ten2.txt -time -ele 8 section 2 fiber 177.0 9.0 1022 stressStrain
recorder Element -file Output/story1_SS_EC_Comp3.txt -time -ele 1 section 3 fiber -180.0 0.0 13 stressStrain
recorder Element -file Output/story1_SS_CC_Comp3.txt -time -ele 1 section 3 fiber -176.0 0.0 33 stressStrain
recorder Element -file Output/story1_SS_ES_Comp3.txt -time -ele 1 section 3 fiber -177.0 9.0 1033 stressStrain
recorder Element -file Output/story1_SS_EC_Ten3.txt -time -ele 1 section 3 fiber 180.0 0.0 13 stressStrain
recorder Element -file Output/story1_SS_CC_Ten3.txt -time -ele 1 section 3 fiber 176.0 0.0 33 stressStrain
recorder Element -file Output/story1_SS_ES_Ten3.txt -time -ele 1 section 3 fiber 177.0 9.0 1033 stressStrain
recorder Element -file Output/story2_SS_EC_Comp3.txt -time -ele 2 section 3 fiber -180.0 0.0 23 stressStrain
recorder Element -file Output/story2_SS_CC_Comp3.txt -time -ele 2 section 3 fiber -176.0 0.0 43 stressStrain
recorder Element -file Output/story2_SS_ES_Comp3.txt -time -ele 2 section 3 fiber -177.0 9.0 1043 stressStrain
recorder Element -file Output/story2_SS_EC_Ten3.txt -time -ele 2 section 3 fiber 180.0 0.0 23 stressStrain
recorder Element -file Output/story2_SS_CC_Ten3.txt -time -ele 2 section 3 fiber 176.0 0.0 43 stressStrain
recorder Element -file Output/story2_SS_ES_Ten3.txt -time -ele 2 section 3 fiber 177.0 9.0 1043 stressStrain
recorder Element -file Output/story3_SS_EC_Comp3.txt -time -ele 3 section 3 fiber -180.0 0.0 23 stressStrain
recorder Element -file Output/story3_SS_CC_Comp3.txt -time -ele 3 section 3 fiber -176.0 0.0 43 stressStrain
recorder Element -file Output/story3_SS_ES_Comp3.txt -time -ele 3 section 3 fiber -177.0 9.0 1043 stressStrain
recorder Element -file Output/story3_SS_EC_Ten3.txt -time -ele 3 section 3 fiber 180.0 0.0 23 stressStrain
recorder Element -file Output/story3_SS_CC_Ten3.txt -time -ele 3 section 3 fiber 176.0 0.0 43 stressStrain
recorder Element -file Output/story3_SS_ES_Ten3.txt -time -ele 3 section 3 fiber 177.0 9.0 1043 stressStrain
recorder Element -file Output/story4_SS_EC_Comp3.txt -time -ele 4 section 3 fiber -180.0 0.0 23 stressStrain
recorder Element -file Output/story4_SS_CC_Comp3.txt -time -ele 4 section 3 fiber -176.0 0.0 43 stressStrain
recorder Element -file Output/story4_SS_ES_Comp3.txt -time -ele 4 section 3 fiber -177.0 9.0 1043 stressStrain
recorder Element -file Output/story4_SS_EC_Ten3.txt -time -ele 4 section 3 fiber 180.0 0.0 23 stressStrain
recorder Element -file Output/story4_SS_CC_Ten3.txt -time -ele 4 section 3 fiber 176.0 0.0 43 stressStrain
recorder Element -file Output/story4_SS_ES_Ten3.txt -time -ele 4 section 3 fiber 177.0 9.0 1043 stressStrain
recorder Element -file Output/story5_SS_EC_Comp3.txt -time -ele 5 section 3 fiber -180.0 0.0 23 stressStrain
recorder Element -file Output/story5_SS_CC_Comp3.txt -time -ele 5 section 3 fiber -176.0 0.0 43 stressStrain
recorder Element -file Output/story5_SS_ES_Comp3.txt -time -ele 5 section 3 fiber -177.0 9.0 1043 stressStrain
recorder Element -file Output/story5_SS_EC_Ten3.txt -time -ele 5 section 3 fiber 180.0 0.0 23 stressStrain
recorder Element -file Output/story5_SS_CC_Ten3.txt -time -ele 5 section 3 fiber 176.0 0.0 43 stressStrain
recorder Element -file Output/story5_SS_ES_Ten3.txt -time -ele 5 section 3 fiber 177.0 9.0 1043 stressStrain
recorder Element -file Output/story6_SS_EC_Comp3.txt -time -ele 6 section 3 fiber -180.0 0.0 23 stressStrain
recorder Element -file Output/story6_SS_ES_Comp3.txt -time -ele 6 section 3 fiber -177.0 9.0 1023 stressStrain
recorder Element -file Output/story6_SS_EC_Ten3.txt -time -ele 6 section 3 fiber 180.0 0.0 23 stressStrain
recorder Element -file Output/story6_SS_ES_Ten3.txt -time -ele 6 section 3 fiber 177.0 9.0 1023 stressStrain
recorder Element -file Output/story7_SS_EC_Comp3.txt -time -ele 7 section 3 fiber -180.0 0.0 23 stressStrain
recorder Element -file Output/story7_SS_ES_Comp3.txt -time -ele 7 section 3 fiber -177.0 9.0 1023 stressStrain
recorder Element -file Output/story7_SS_EC_Ten3.txt -time -ele 7 section 3 fiber 180.0 0.0 23 stressStrain
recorder Element -file Output/story7_SS_ES_Ten3.txt -time -ele 7 section 3 fiber 177.0 9.0 1023 stressStrain
recorder Element -file Output/story8_SS_EC_Comp3.txt -time -ele 8 section 3 fiber -180.0 0.0 23 stressStrain
recorder Element -file Output/story8_SS_ES_Comp3.txt -time -ele 8 section 3 fiber -177.0 9.0 1023 stressStrain
recorder Element -file Output/story8_SS_EC_Ten3.txt -time -ele 8 section 3 fiber 180.0 0.0 23 stressStrain
recorder Element -file Output/story8_SS_ES_Ten3.txt -time -ele 8 section 3 fiber 177.0 9.0 1023 stressStrain
recorder Node  -file Output/node1R_regular.txt -time -node 1 -dof 1 2 3 reaction
recorder Node  -file Output/nodeDisp_regular.txt -time -node 2 3 4 5 6 7 8 9 -dof 1 2 3 disp
recorder Element -file Output/WallForces_regular.txt -time -ele 1 2 3 4 5 6 7 8 globalForce
recorder Element -file Output/SectionCurvature1_regular1.txt -time -ele 1 section 1 deformation
recorder Element -file Output/SectionMoment1_regular1.txt -time -ele 1 section 1 force
recorder Element -file Output/SectionCurvature1_regular2.txt -time -ele 1 section 2 deformation
recorder Element -file Output/SectionMoment1_regular2.txt -time -ele 1 section 2 force
recorder Element -file Output/SectionCurvature1_regular3.txt -time -ele 1 section 3 deformation
recorder Element -file Output/SectionMoment1_regular3.txt -time -ele 1 section 3 force
recorder Element -file Output/SectionCurvature1_regular4.txt -time -ele 1 section 4 deformation
recorder Element -file Output/SectionMoment1_regular4.txt -time -ele 1 section 4 force
recorder Element -file Output/SectionCurvature1_regular5.txt -time -ele 1 section 5 deformation
recorder Element -file Output/SectionMoment1_regular5.txt -time -ele 1 section 5 force
recorder Element -file Output/SectionCurvature2_regular1.txt -time -ele 2 section 1 deformation
recorder Element -file Output/SectionMoment2_regular1.txt -time -ele 2 section 1 force
recorder Element -file Output/SectionCurvature2_regular2.txt -time -ele 2 section 2 deformation
recorder Element -file Output/SectionMoment2_regular2.txt -time -ele 2 section 2 force
recorder Element -file Output/SectionCurvature2_regular3.txt -time -ele 2 section 3 deformation
recorder Element -file Output/SectionMoment2_regular3.txt -time -ele 2 section 3 force
recorder Element -file Output/SectionCurvature2_regular4.txt -time -ele 2 section 4 deformation
recorder Element -file Output/SectionMoment2_regular4.txt -time -ele 2 section 4 force
recorder Element -file Output/SectionCurvature2_regular5.txt -time -ele 2 section 5 deformation
recorder Element -file Output/SectionMoment2_regular5.txt -time -ele 2 section 5 force
recorder Element -file Output/SectionCurvature3_regular1.txt -time -ele 3 section 1 deformation
recorder Element -file Output/SectionMoment3_regular1.txt -time -ele 3 section 1 force
recorder Element -file Output/SectionCurvature3_regular2.txt -time -ele 3 section 2 deformation
recorder Element -file Output/SectionMoment3_regular2.txt -time -ele 3 section 2 force
recorder Element -file Output/SectionCurvature3_regular3.txt -time -ele 3 section 3 deformation
recorder Element -file Output/SectionMoment3_regular3.txt -time -ele 3 section 3 force
recorder Element -file Output/SectionCurvature3_regular4.txt -time -ele 3 section 4 deformation
recorder Element -file Output/SectionMoment3_regular4.txt -time -ele 3 section 4 force
recorder Element -file Output/SectionCurvature3_regular5.txt -time -ele 3 section 5 deformation
recorder Element -file Output/SectionMoment3_regular5.txt -time -ele 3 section 5 force
recorder Element -file Output/SectionCurvature4_regular1.txt -time -ele 4 section 1 deformation
recorder Element -file Output/SectionMoment4_regular1.txt -time -ele 4 section 1 force
recorder Element -file Output/SectionCurvature4_regular2.txt -time -ele 4 section 2 deformation
recorder Element -file Output/SectionMoment4_regular2.txt -time -ele 4 section 2 force
recorder Element -file Output/SectionCurvature4_regular3.txt -time -ele 4 section 3 deformation
recorder Element -file Output/SectionMoment4_regular3.txt -time -ele 4 section 3 force
recorder Element -file Output/SectionCurvature4_regular4.txt -time -ele 4 section 4 deformation
recorder Element -file Output/SectionMoment4_regular4.txt -time -ele 4 section 4 force
recorder Element -file Output/SectionCurvature4_regular5.txt -time -ele 4 section 5 deformation
recorder Element -file Output/SectionMoment4_regular5.txt -time -ele 4 section 5 force
recorder Element -file Output/SectionCurvature5_regular1.txt -time -ele 5 section 1 deformation
recorder Element -file Output/SectionMoment5_regular1.txt -time -ele 5 section 1 force
recorder Element -file Output/SectionCurvature5_regular2.txt -time -ele 5 section 2 deformation
recorder Element -file Output/SectionMoment5_regular2.txt -time -ele 5 section 2 force
recorder Element -file Output/SectionCurvature5_regular3.txt -time -ele 5 section 3 deformation
recorder Element -file Output/SectionMoment5_regular3.txt -time -ele 5 section 3 force
recorder Element -file Output/SectionCurvature5_regular4.txt -time -ele 5 section 4 deformation
recorder Element -file Output/SectionMoment5_regular4.txt -time -ele 5 section 4 force
recorder Element -file Output/SectionCurvature5_regular5.txt -time -ele 5 section 5 deformation
recorder Element -file Output/SectionMoment5_regular5.txt -time -ele 5 section 5 force
recorder Element -file Output/SectionCurvature6_regular1.txt -time -ele 6 section 1 deformation
recorder Element -file Output/SectionMoment6_regular1.txt -time -ele 6 section 1 force
recorder Element -file Output/SectionCurvature6_regular2.txt -time -ele 6 section 2 deformation
recorder Element -file Output/SectionMoment6_regular2.txt -time -ele 6 section 2 force
recorder Element -file Output/SectionCurvature6_regular3.txt -time -ele 6 section 3 deformation
recorder Element -file Output/SectionMoment6_regular3.txt -time -ele 6 section 3 force
recorder Element -file Output/SectionCurvature6_regular4.txt -time -ele 6 section 4 deformation
recorder Element -file Output/SectionMoment6_regular4.txt -time -ele 6 section 4 force
recorder Element -file Output/SectionCurvature6_regular5.txt -time -ele 6 section 5 deformation
recorder Element -file Output/SectionMoment6_regular5.txt -time -ele 6 section 5 force
recorder Element -file Output/SectionCurvature7_regular1.txt -time -ele 7 section 1 deformation
recorder Element -file Output/SectionMoment7_regular1.txt -time -ele 7 section 1 force
recorder Element -file Output/SectionCurvature7_regular2.txt -time -ele 7 section 2 deformation
recorder Element -file Output/SectionMoment7_regular2.txt -time -ele 7 section 2 force
recorder Element -file Output/SectionCurvature7_regular3.txt -time -ele 7 section 3 deformation
recorder Element -file Output/SectionMoment7_regular3.txt -time -ele 7 section 3 force
recorder Element -file Output/SectionCurvature7_regular4.txt -time -ele 7 section 4 deformation
recorder Element -file Output/SectionMoment7_regular4.txt -time -ele 7 section 4 force
recorder Element -file Output/SectionCurvature7_regular5.txt -time -ele 7 section 5 deformation
recorder Element -file Output/SectionMoment7_regular5.txt -time -ele 7 section 5 force
recorder Element -file Output/SectionCurvature8_regular1.txt -time -ele 8 section 1 deformation
recorder Element -file Output/SectionMoment8_regular1.txt -time -ele 8 section 1 force
recorder Element -file Output/SectionCurvature8_regular2.txt -time -ele 8 section 2 deformation
recorder Element -file Output/SectionMoment8_regular2.txt -time -ele 8 section 2 force
recorder Element -file Output/SectionCurvature8_regular3.txt -time -ele 8 section 3 deformation
recorder Element -file Output/SectionMoment8_regular3.txt -time -ele 8 section 3 force
recorder Element -file Output/SectionCurvature8_regular4.txt -time -ele 8 section 4 deformation
recorder Element -file Output/SectionMoment8_regular4.txt -time -ele 8 section 4 force
recorder Element -file Output/SectionCurvature8_regular5.txt -time -ele 8 section 5 deformation
recorder Element -file Output/SectionMoment8_regular5.txt -time -ele 8 section 5 force
# ------------------------------
# End of model generation
# ------------------------------
# ------------------------------
# Start of analysis
# ------------------------------
# Define gravity loads
# --------------------
# Set a parameter for the axial load
pattern Plain 1 "Linear" {
	load 2  0.0 -263340.0  0.0
	load 3  0.0 -263340.0  0.0
	load 4  0.0 -263340.0  0.0
	load 5  0.0 -263340.0  0.0
	load 6  0.0 -263340.0  0.0
	load 7  0.0 -263340.0  0.0
	load 8  0.0 -263340.0  0.0
	load 9  0.0 -204468.0  0.0
}
set Tol 1.0e-8;						# convergence tolerance for test
constraints Plain;   				# how it handles boundary conditions
numberer Plain;	# renumber dofs to minimize band-width (optimization) + if you want to
system BandGeneral;					# how to store and solve the system of equations in the analysis
test NormDispIncr $Tol 10; 		# determine if convergence has been achieved at the end of an iteration step
algorithm Newton;					# use Newtons solution algorithm: updates tangent stiffness at every iteration
set NstepGravity 10; 				# apply gravity in 10 steps
set DGravity [expr 1./$NstepGravity]; 	# first load increment
integrator LoadControl $DGravity;	# determine the next time step for an analysis
analysis Static;					# define type of analysis static or transient
analyze $NstepGravity	;			# apply gravity
# ------------------------------------------------- maintain constant gravity loads and reset time to zero
loadConst -time 0.0;
pattern Plain 12 Linear {				# define load pattern -- generalized
	load 9 [expr 211./1534.] 0.0 0.0 
	load 8 [expr 238./1534.] 0.0 0.0 
	load 7 [expr 205./1534.] 0.0 0.0 
	load 6 [expr 172./1534.] 0.0 0.0 
	load 5 [expr 138./1534.] 0.0 0.0 
	load 4 [expr 105./1534.] 0.0 0.0 
	load 3 [expr 72./1534.] 0.0 0.0 
	load 2 [expr 38./1534.] 0.0 0.0 
}
set globalTol 0.0001 ;
constraints Transformation;
numberer RCM;
system ProfileSPD;
set globalSolutionTol $globalTol;
set numIter	35;
set printFlagStatic 0;
test NormUnbalance $globalSolutionTol $numIter $printFlagStatic;
algorithm Newton;
set nodeTag 9;					# node where displacement is read for displacement control
set dofTag 1;					# degree of freedom of displacement read for displacement contro
set Dmax [expr 0.05*[expr (15.0 + 13.0*7.0)*12.0]];
set Dincr [expr 0.01*$Dmax];		# displacement increment for pushover. you want this to be very small + but not too small to slow down the analysis
set minDu [expr 0.00001*$Dincr];
set maxDu $Dincr;
set dU1 $Dincr;
integrator DisplacementControl $nodeTag $dofTag $dU1 4 $minDu $maxDu;
analysis Static;
set nSteps [expr int($Dmax/$dU1)];
# --- Set initial variables ---
set uDemand 0; set duDemand 0;
set ok 0; set linearFlag 0; set stepCount 0; set stepKill 2000;
# ---------------------------------  perform Static Pushover Analysis;
# set Nsteps [expr int($Dmax/$Dincr)];    # number of pushover analysis steps;
# set ok [analyze $Nsteps];        # this will return zero if no convergence problems were encountered;
puts "Model Built"
#
# Perform Analysis -----------------------------------------------------------------------------------
while {$ok == 0 && $uDemand < $Dmax && $stepCount < $stepKill } {
	set ok [analyze 1 $dU1];	
	set duDemand [nodeDisp $nodeTag $dofTag];
	# if the analysis fails try some other stuff
	if {$ok != 0} {
			puts "***that didnt work - try Modified Newton"
			integrator DisplacementControl $nodeTag $dofTag 0 1 $minDu $minDu
			algorithm Newton -initial
			set ok [analyze 1 $dU1];
			set duDemand [nodeDisp $nodeTag $dofTag];
      if {$ok != 0} {
        puts "***that didnt work - try Newton-Line Search"
        algorithm NewtonLineSearch	0.8
        set ok [analyze 1 $dU1];
        set duDemand [nodeDisp $nodeTag $dofTag];
        if {$ok != 0} {
            puts "***that didnt work - take large step"
            integrator DisplacementControl $nodeTag $dofTag 0 4 [expr $minDu*20] [expr $maxDu*20]
            test NormDispIncr 1e-3 [expr $numIter] 2
            algorithm Newton
            set ok [analyze 1 [expr $minDu*5.]];
            set duDemand [nodeDisp $nodeTag $dofTag];
          if {$ok != 0} {
            puts "***that didnt work - take large step"
            integrator DisplacementControl $nodeTag $dofTag 0 4 [expr $minDu*20] [expr $maxDu*20]
            test NormDispIncr 1e-3 [expr $numIter] 2
            algorithm Newton
            set ok [analyze 1 [expr $minDu*5.]];
            set duDemand [nodeDisp $nodeTag $dofTag];
            if {$ok != 0} {
              puts "***that didnt work - take small step"
              integrator DisplacementControl $nodeTag $dofTag 0 4 [expr $minDu/100] [expr $maxDu/100]
              test NormDispIncr 1e-3 [expr $numIter] 2
              set ok [analyze 1 [expr $minDu/100.]];
              set duDemand [nodeDisp $nodeTag $dofTag];
              if {$ok != 0} {
                puts "***that didnt work - take linear step"
                set linearFlag 1;
                test NormDispIncr 1e-3 [expr $numIter*2] 2
                algorithm Linear
                set ok [analyze 1 $minDu];
                set duDemand [nodeDisp $nodeTag $dofTag];
              }
            }
          }
}
      }
		if {$ok == 0} {
			puts "***... back to regular Newton"
			integrator DisplacementControl $nodeTag $dofTag 0 4 [expr $minDu] [expr $maxDu]
			test NormDispIncr [expr $globalSolutionTol] $numIter $printFlagStatic
			algorithm Newton
		}
	}
	set uDemand [expr $duDemand];				# update new Ui
	set stepCount [expr $stepCount + 1];		# update the step number
	puts "stepCount $stepCount"
}
# Window Outputs -----------------------------------------------------------------------------------------------------
puts " "
puts "=================================================================================="
puts "================================= Analysis Ended ================================="
puts "=================================================================================="
puts " "
if {$ok != 0} {
	puts "target displacement NOT achieved"
} elseif {$linearFlag == 1} {
	puts "target displacement achieved but required linear steps"
} else {
	puts "target displacement achieved successfully"
}
wipe
