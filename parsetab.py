
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightCOMMArightEQUALleftORleftANDleftEQUALITYleftLESSGREATERleftPLUSMINUSleftTIMESDIVIDEAND BOOL CINT COMMA DEF DIVIDE DOLLAR ELSE EQUAL EQUALITY EXTERN FALSE FLOAT GREATER ID IF INT LBRACE LBRACKET LESS LPAREN MINUS NOALIAS NOT NUMBER OR PLUS PRINT RBRACE RBRACKET REF RETURN RPAREN SEMICOLON SLIT TIMES TRUE VOID WHILE\n    PROG : FUNCS\n        | EXTERNS FUNCS\n    \n    EXTERNS : EXTERNSTS \n            | EXTERNS EXTERNSTS\n    \n    FUNCS : FUNC\n        | FUNCS FUNC\n    \n    EXTERNSTS : EXTERN TYPE ID LPAREN RPAREN SEMICOLON\n            | EXTERN TYPE ID LPAREN TDECLS RPAREN SEMICOLON\n    \n    FUNC : DEF TYPE ID LPAREN RPAREN BLK\n    FUNC : DEF TYPE ID LPAREN VDECLS RPAREN BLK\n    \n    BLK : LBRACE RBRACE\n    BLK : LBRACE STMTS RBRACE\n    \n    STMTS : STMT\n    STMTS : STMTS STMT\n    STMT : BLK\n    STMT : RETURN SEMICOLON \n         | RETURN EXP SEMICOLON\n    \n    STMT : VDECL EQUAL EXP SEMICOLON\n    \n    STMT : EXP SEMICOLON\n    \n    STMT : WHILE LPAREN EXP RPAREN STMT\n    \n    STMT : IF LPAREN EXP RPAREN STMT\n         | IF LPAREN EXP RPAREN STMT ELSE STMT\n    \n    STMT : PRINT EXP SEMICOLON\n    \n    STMT : PRINT SLIT SEMICOLON\n    EXPS : EXP\n            | EXPS COMMA EXPEXP : EXPPAREN\n            | BINOP\n            | UOP\n            | LIT\n            | VARID\n            | EXPGLOBIDEXPPAREN : LPAREN EXP RPARENEXPGLOBID : GLOBID EXPWRAPPEREXPWRAPPER : LPAREN RPAREN\n                | LPAREN EXPS RPARENASSIGN : VARID EQUAL EXPTYPECAST : LBRACKET TYPE RBRACKET EXPBINOP : ARITHOPS\n            | LOGICOPS\n            | ASSIGN\n            | TYPECASTARITHOPS : EXP TIMES EXP\n                | EXP DIVIDE EXP\n                | EXP PLUS EXP\n                | EXP MINUS EXPLOGICOPS : EXP EQUALITY EXP\n                | EXP LESS EXP\n                | EXP GREATER EXP\n                | EXP AND EXP\n                | EXP OR EXPUOP : NOT EXP\n            | MINUS EXPLIT : TRUE\n            | FALSE\n            | NUMBERTDECLS : TYPE\n                | TDECLS COMMA TYPEVDECLS : VDECLS COMMA VDECL\n            | VDECLVDECL : TYPE VARIDVARID : DOLLAR IDTYPE : INT\n          | FLOAT\n          | CINT\n          | VOIDTYPE : REF TYPETYPE : NOALIAS REF TYPEGLOBID : ID'
    
_lr_action_items = {'DEF':([0,2,3,4,5,8,9,10,35,39,43,72,74,76,],[6,6,6,-5,-3,-6,6,-4,-9,-7,-11,-10,-8,-12,]),'EXTERN':([0,3,5,10,39,74,],[7,7,-3,-4,-7,-8,]),'$end':([1,2,4,8,9,35,43,72,76,],[0,-1,-5,-6,-2,-9,-11,-10,-12,]),'INT':([6,7,16,21,23,25,36,38,41,43,44,45,46,71,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[12,12,12,12,12,12,12,12,12,-11,12,-13,-15,12,-12,-14,-16,-19,-17,-23,-24,-18,12,12,-20,-21,12,-22,]),'FLOAT':([6,7,16,21,23,25,36,38,41,43,44,45,46,71,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[13,13,13,13,13,13,13,13,13,-11,13,-13,-15,13,-12,-14,-16,-19,-17,-23,-24,-18,13,13,-20,-21,13,-22,]),'CINT':([6,7,16,21,23,25,36,38,41,43,44,45,46,71,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[14,14,14,14,14,14,14,14,14,-11,14,-13,-15,14,-12,-14,-16,-19,-17,-23,-24,-18,14,14,-20,-21,14,-22,]),'VOID':([6,7,16,21,23,25,36,38,41,43,44,45,46,71,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[15,15,15,15,15,15,15,15,15,-11,15,-13,-15,15,-12,-14,-16,-19,-17,-23,-24,-18,15,15,-20,-21,15,-22,]),'REF':([6,7,16,17,21,23,25,36,38,41,43,44,45,46,71,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[16,16,16,21,16,16,16,16,16,16,-11,16,-13,-15,16,-12,-14,-16,-19,-17,-23,-24,-18,16,16,-20,-21,16,-22,]),'NOALIAS':([6,7,16,21,23,25,36,38,41,43,44,45,46,71,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[17,17,17,17,17,17,17,17,17,-11,17,-13,-15,17,-12,-14,-16,-19,-17,-23,-24,-18,17,17,-20,-21,17,-22,]),'ID':([11,12,13,14,15,18,20,24,34,36,43,44,45,46,47,51,53,64,65,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,93,96,100,102,116,117,122,123,124,125,127,129,130,132,133,],[19,-63,-64,-65,-66,22,-67,-68,42,69,-11,69,-13,-15,69,69,69,69,69,-12,-14,-16,-19,69,69,69,69,69,69,69,69,69,69,69,69,69,69,-17,-23,-24,69,-18,69,69,69,-20,-21,69,-22,]),'DOLLAR':([12,13,14,15,20,24,26,36,43,44,45,46,47,51,53,64,65,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,93,96,100,102,116,117,122,123,124,125,127,129,130,132,133,],[-63,-64,-65,-66,-67,-68,34,34,-11,34,-13,-15,34,34,34,34,34,-12,-14,-16,-19,34,34,34,34,34,34,34,34,34,34,34,34,34,34,-17,-23,-24,34,-18,34,34,34,-20,-21,34,-22,]),'RPAREN':([12,13,14,15,20,23,24,25,28,29,30,32,33,42,54,55,56,57,58,59,60,61,62,63,66,67,68,73,75,92,97,98,99,100,103,104,105,106,107,108,109,110,111,113,114,115,118,119,120,121,126,128,131,],[-63,-64,-65,-66,-67,27,-68,31,37,-60,-57,40,-61,-62,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,-59,-58,114,-52,-53,-34,119,-43,-44,-45,-46,-47,-48,-49,-50,-51,124,-33,125,-37,-35,126,-25,-36,-38,-26,]),'COMMA':([12,13,14,15,20,24,28,29,30,32,33,42,54,55,56,57,58,59,60,61,62,63,66,67,68,73,75,97,98,99,103,104,105,106,107,108,109,110,111,114,118,119,120,121,126,128,131,],[-63,-64,-65,-66,-67,-68,38,-60,-57,41,-61,-62,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,-59,-58,-52,-53,-34,-43,-44,-45,-46,-47,-48,-49,-50,-51,-33,-37,-35,127,-25,-36,-38,-26,]),'RBRACKET':([12,13,14,15,20,24,101,],[-63,-64,-65,-66,-67,-68,122,]),'LPAREN':([19,22,36,43,44,45,46,47,50,51,52,53,64,65,69,70,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,93,96,100,102,116,117,122,123,124,125,127,129,130,132,133,],[23,25,51,-11,51,-13,-15,51,91,51,93,51,51,51,-69,100,-12,-14,-16,-19,51,51,51,51,51,51,51,51,51,51,51,51,51,51,-17,-23,-24,51,-18,51,51,51,-20,-21,51,-22,]),'LBRACE':([27,36,37,43,44,45,46,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[36,36,36,-11,36,-13,-15,-12,-14,-16,-19,-17,-23,-24,-18,36,36,-20,-21,36,-22,]),'SEMICOLON':([31,40,42,47,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,94,95,97,98,99,103,104,105,106,107,108,109,110,111,112,114,118,119,126,128,],[39,74,-62,78,80,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,102,116,117,-52,-53,-34,-43,-44,-45,-46,-47,-48,-49,-50,-51,123,-33,-37,-35,-36,-38,]),'EQUAL':([33,42,49,54,],[-61,-62,90,96,]),'RBRACE':([36,43,44,45,46,76,77,78,80,102,116,117,123,129,130,133,],[43,-11,76,-13,-15,-12,-14,-16,-19,-17,-23,-24,-18,-20,-21,-22,]),'RETURN':([36,43,44,45,46,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[47,-11,47,-13,-15,-12,-14,-16,-19,-17,-23,-24,-18,47,47,-20,-21,47,-22,]),'WHILE':([36,43,44,45,46,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[50,-11,50,-13,-15,-12,-14,-16,-19,-17,-23,-24,-18,50,50,-20,-21,50,-22,]),'IF':([36,43,44,45,46,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[52,-11,52,-13,-15,-12,-14,-16,-19,-17,-23,-24,-18,52,52,-20,-21,52,-22,]),'PRINT':([36,43,44,45,46,76,77,78,80,102,116,117,123,124,125,129,130,132,133,],[53,-11,53,-13,-15,-12,-14,-16,-19,-17,-23,-24,-18,53,53,-20,-21,53,-22,]),'NOT':([36,43,44,45,46,47,51,53,64,65,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,93,96,100,102,116,117,122,123,124,125,127,129,130,132,133,],[64,-11,64,-13,-15,64,64,64,64,64,-12,-14,-16,-19,64,64,64,64,64,64,64,64,64,64,64,64,64,64,-17,-23,-24,64,-18,64,64,64,-20,-21,64,-22,]),'MINUS':([36,42,43,44,45,46,47,48,51,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,96,97,98,99,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,121,122,123,124,125,126,127,128,129,130,131,132,133,],[65,-62,-11,65,-13,-15,65,84,65,65,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,65,65,-54,-55,-56,-12,-14,-16,84,-19,65,65,65,65,65,65,65,65,65,65,65,84,65,84,65,84,-53,-34,65,-17,-43,-44,-45,-46,84,84,84,84,84,84,84,-33,84,-23,-24,84,-35,84,65,-18,65,65,-36,65,84,-20,-21,84,65,-22,]),'TRUE':([36,43,44,45,46,47,51,53,64,65,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,93,96,100,102,116,117,122,123,124,125,127,129,130,132,133,],[66,-11,66,-13,-15,66,66,66,66,66,-12,-14,-16,-19,66,66,66,66,66,66,66,66,66,66,66,66,66,66,-17,-23,-24,66,-18,66,66,66,-20,-21,66,-22,]),'FALSE':([36,43,44,45,46,47,51,53,64,65,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,93,96,100,102,116,117,122,123,124,125,127,129,130,132,133,],[67,-11,67,-13,-15,67,67,67,67,67,-12,-14,-16,-19,67,67,67,67,67,67,67,67,67,67,67,67,67,67,-17,-23,-24,67,-18,67,67,67,-20,-21,67,-22,]),'NUMBER':([36,43,44,45,46,47,51,53,64,65,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,93,96,100,102,116,117,122,123,124,125,127,129,130,132,133,],[68,-11,68,-13,-15,68,68,68,68,68,-12,-14,-16,-19,68,68,68,68,68,68,68,68,68,68,68,68,68,68,-17,-23,-24,68,-18,68,68,68,-20,-21,68,-22,]),'LBRACKET':([36,43,44,45,46,47,51,53,64,65,76,77,78,80,81,82,83,84,85,86,87,88,89,90,91,93,96,100,102,116,117,122,123,124,125,127,129,130,132,133,],[71,-11,71,-13,-15,71,71,71,71,71,-12,-14,-16,-19,71,71,71,71,71,71,71,71,71,71,71,71,71,71,-17,-23,-24,71,-18,71,71,71,-20,-21,71,-22,]),'TIMES':([42,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,92,94,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,118,119,121,126,128,131,],[-62,81,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,81,81,81,81,81,-34,-43,-44,81,81,81,81,81,81,81,81,81,-33,81,81,-35,81,-36,81,81,]),'DIVIDE':([42,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,92,94,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,118,119,121,126,128,131,],[-62,82,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,82,82,82,82,82,-34,-43,-44,82,82,82,82,82,82,82,82,82,-33,82,82,-35,82,-36,82,82,]),'PLUS':([42,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,92,94,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,118,119,121,126,128,131,],[-62,83,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,83,83,83,83,-53,-34,-43,-44,-45,-46,83,83,83,83,83,83,83,-33,83,83,-35,83,-36,83,83,]),'EQUALITY':([42,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,92,94,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,118,119,121,126,128,131,],[-62,85,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,85,85,85,85,-53,-34,-43,-44,-45,-46,-47,-48,-49,85,85,85,85,-33,85,85,-35,85,-36,85,85,]),'LESS':([42,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,92,94,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,118,119,121,126,128,131,],[-62,86,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,86,86,86,86,-53,-34,-43,-44,-45,-46,86,-48,-49,86,86,86,86,-33,86,86,-35,86,-36,86,86,]),'GREATER':([42,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,92,94,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,118,119,121,126,128,131,],[-62,87,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,87,87,87,87,-53,-34,-43,-44,-45,-46,87,-48,-49,87,87,87,87,-33,87,87,-35,87,-36,87,87,]),'AND':([42,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,92,94,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,118,119,121,126,128,131,],[-62,88,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,88,88,88,88,-53,-34,-43,-44,-45,-46,-47,-48,-49,-50,88,88,88,-33,88,88,-35,88,-36,88,88,]),'OR':([42,48,54,55,56,57,58,59,60,61,62,63,66,67,68,79,92,94,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,118,119,121,126,128,131,],[-62,89,-31,-27,-28,-29,-30,-32,-39,-40,-41,-42,-54,-55,-56,89,89,89,89,-53,-34,-43,-44,-45,-46,-47,-48,-49,-50,-51,89,89,-33,89,89,-35,89,-36,89,89,]),'ELSE':([43,46,76,78,80,102,116,117,123,129,130,133,],[-11,-15,-12,-16,-19,-17,-23,-24,-18,-20,132,-22,]),'SLIT':([53,],[95,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'PROG':([0,],[1,]),'FUNCS':([0,3,],[2,9,]),'EXTERNS':([0,],[3,]),'FUNC':([0,2,3,9,],[4,8,4,8,]),'EXTERNSTS':([0,3,],[5,10,]),'TYPE':([6,7,16,21,23,25,36,38,41,44,71,124,125,132,],[11,18,20,24,26,30,26,26,75,26,101,26,26,26,]),'VDECLS':([23,],[28,]),'VDECL':([23,36,38,44,124,125,132,],[29,49,73,49,49,49,49,]),'TDECLS':([25,],[32,]),'VARID':([26,36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[33,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,54,]),'BLK':([27,36,37,44,124,125,132,],[35,46,72,46,46,46,46,]),'STMTS':([36,],[44,]),'STMT':([36,44,124,125,132,],[45,77,129,130,133,]),'EXP':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[48,48,79,92,94,97,98,103,104,105,106,107,108,109,110,111,112,113,115,118,121,128,48,48,131,48,]),'EXPPAREN':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'BINOP':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'UOP':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'LIT':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,58,]),'EXPGLOBID':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,]),'ARITHOPS':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,]),'LOGICOPS':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,]),'ASSIGN':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,]),'TYPECAST':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,]),'GLOBID':([36,44,47,51,53,64,65,81,82,83,84,85,86,87,88,89,90,91,93,96,100,122,124,125,127,132,],[70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,]),'EXPWRAPPER':([70,],[99,]),'EXPS':([100,],[120,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> PROG","S'",1,None,None,None),
  ('PROG -> FUNCS','PROG',1,'p_prog','parser.py',836),
  ('PROG -> EXTERNS FUNCS','PROG',2,'p_prog','parser.py',837),
  ('EXTERNS -> EXTERNSTS','EXTERNS',1,'p_externs','parser.py',853),
  ('EXTERNS -> EXTERNS EXTERNSTS','EXTERNS',2,'p_externs','parser.py',854),
  ('FUNCS -> FUNC','FUNCS',1,'p_funcs','parser.py',865),
  ('FUNCS -> FUNCS FUNC','FUNCS',2,'p_funcs','parser.py',866),
  ('EXTERNSTS -> EXTERN TYPE ID LPAREN RPAREN SEMICOLON','EXTERNSTS',6,'p_extern','parser.py',876),
  ('EXTERNSTS -> EXTERN TYPE ID LPAREN TDECLS RPAREN SEMICOLON','EXTERNSTS',7,'p_extern','parser.py',877),
  ('FUNC -> DEF TYPE ID LPAREN RPAREN BLK','FUNC',6,'p_func','parser.py',889),
  ('FUNC -> DEF TYPE ID LPAREN VDECLS RPAREN BLK','FUNC',7,'p_func','parser.py',890),
  ('BLK -> LBRACE RBRACE','BLK',2,'p_blk','parser.py',929),
  ('BLK -> LBRACE STMTS RBRACE','BLK',3,'p_blk','parser.py',930),
  ('STMTS -> STMT','STMTS',1,'p_stmts','parser.py',940),
  ('STMTS -> STMTS STMT','STMTS',2,'p_stmts','parser.py',941),
  ('STMT -> BLK','STMT',1,'p_stmt_blk','parser.py',950),
  ('STMT -> RETURN SEMICOLON','STMT',2,'p_stmt_ret','parser.py',955),
  ('STMT -> RETURN EXP SEMICOLON','STMT',3,'p_stmt_ret','parser.py',956),
  ('STMT -> VDECL EQUAL EXP SEMICOLON','STMT',4,'p_stmt_vdecl','parser.py',965),
  ('STMT -> EXP SEMICOLON','STMT',2,'p_stmt_expSemi','parser.py',971),
  ('STMT -> WHILE LPAREN EXP RPAREN STMT','STMT',5,'p_stmt_while','parser.py',977),
  ('STMT -> IF LPAREN EXP RPAREN STMT','STMT',5,'p_stmt_if','parser.py',983),
  ('STMT -> IF LPAREN EXP RPAREN STMT ELSE STMT','STMT',7,'p_stmt_if','parser.py',984),
  ('STMT -> PRINT EXP SEMICOLON','STMT',3,'p_stmt_print_exp','parser.py',993),
  ('STMT -> PRINT SLIT SEMICOLON','STMT',3,'p_stmt_print_slit','parser.py',999),
  ('EXPS -> EXP','EXPS',1,'p_exps','parser.py',1004),
  ('EXPS -> EXPS COMMA EXP','EXPS',3,'p_exps','parser.py',1005),
  ('EXP -> EXPPAREN','EXP',1,'p_exp','parser.py',1013),
  ('EXP -> BINOP','EXP',1,'p_exp','parser.py',1014),
  ('EXP -> UOP','EXP',1,'p_exp','parser.py',1015),
  ('EXP -> LIT','EXP',1,'p_exp','parser.py',1016),
  ('EXP -> VARID','EXP',1,'p_exp','parser.py',1017),
  ('EXP -> EXPGLOBID','EXP',1,'p_exp','parser.py',1018),
  ('EXPPAREN -> LPAREN EXP RPAREN','EXPPAREN',3,'p_expParen','parser.py',1022),
  ('EXPGLOBID -> GLOBID EXPWRAPPER','EXPGLOBID',2,'p_expGlobid','parser.py',1026),
  ('EXPWRAPPER -> LPAREN RPAREN','EXPWRAPPER',2,'p_expWrapper','parser.py',1030),
  ('EXPWRAPPER -> LPAREN EXPS RPAREN','EXPWRAPPER',3,'p_expWrapper','parser.py',1031),
  ('ASSIGN -> VARID EQUAL EXP','ASSIGN',3,'p_assign','parser.py',1038),
  ('TYPECAST -> LBRACKET TYPE RBRACKET EXP','TYPECAST',4,'p_typeCast','parser.py',1042),
  ('BINOP -> ARITHOPS','BINOP',1,'p_binop','parser.py',1046),
  ('BINOP -> LOGICOPS','BINOP',1,'p_binop','parser.py',1047),
  ('BINOP -> ASSIGN','BINOP',1,'p_binop','parser.py',1048),
  ('BINOP -> TYPECAST','BINOP',1,'p_binop','parser.py',1049),
  ('ARITHOPS -> EXP TIMES EXP','ARITHOPS',3,'p_arithOps','parser.py',1053),
  ('ARITHOPS -> EXP DIVIDE EXP','ARITHOPS',3,'p_arithOps','parser.py',1054),
  ('ARITHOPS -> EXP PLUS EXP','ARITHOPS',3,'p_arithOps','parser.py',1055),
  ('ARITHOPS -> EXP MINUS EXP','ARITHOPS',3,'p_arithOps','parser.py',1056),
  ('LOGICOPS -> EXP EQUALITY EXP','LOGICOPS',3,'p_logicOps','parser.py',1067),
  ('LOGICOPS -> EXP LESS EXP','LOGICOPS',3,'p_logicOps','parser.py',1068),
  ('LOGICOPS -> EXP GREATER EXP','LOGICOPS',3,'p_logicOps','parser.py',1069),
  ('LOGICOPS -> EXP AND EXP','LOGICOPS',3,'p_logicOps','parser.py',1070),
  ('LOGICOPS -> EXP OR EXP','LOGICOPS',3,'p_logicOps','parser.py',1071),
  ('UOP -> NOT EXP','UOP',2,'p_uop','parser.py',1084),
  ('UOP -> MINUS EXP','UOP',2,'p_uop','parser.py',1085),
  ('LIT -> TRUE','LIT',1,'p_lit','parser.py',1092),
  ('LIT -> FALSE','LIT',1,'p_lit','parser.py',1093),
  ('LIT -> NUMBER','LIT',1,'p_lit','parser.py',1094),
  ('TDECLS -> TYPE','TDECLS',1,'p_tdecls','parser.py',1098),
  ('TDECLS -> TDECLS COMMA TYPE','TDECLS',3,'p_tdecls','parser.py',1099),
  ('VDECLS -> VDECLS COMMA VDECL','VDECLS',3,'p_vdecls','parser.py',1107),
  ('VDECLS -> VDECL','VDECLS',1,'p_vdecls','parser.py',1108),
  ('VDECL -> TYPE VARID','VDECL',2,'p_vdecl','parser.py',1118),
  ('VARID -> DOLLAR ID','VARID',2,'p_varid','parser.py',1124),
  ('TYPE -> INT','TYPE',1,'p_simpleType','parser.py',1129),
  ('TYPE -> FLOAT','TYPE',1,'p_simpleType','parser.py',1130),
  ('TYPE -> CINT','TYPE',1,'p_simpleType','parser.py',1131),
  ('TYPE -> VOID','TYPE',1,'p_simpleType','parser.py',1132),
  ('TYPE -> REF TYPE','TYPE',2,'p_refType','parser.py',1136),
  ('TYPE -> NOALIAS REF TYPE','TYPE',3,'p_refTypeNoAlias','parser.py',1153),
  ('GLOBID -> ID','GLOBID',1,'p_globid','parser.py',1170),
]
