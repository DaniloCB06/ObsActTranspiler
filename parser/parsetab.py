
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ALERTA AND BOOL COLON COMMA DESLIGAR DISPOSITIVO DOT ENTAO ENVIAR EQUAL LBRACE LIGAR LPAREN MSG NAME NUMBER OPLOGIC PARA RBRACE RPAREN SE SENAO SET TODOSprogram : devices cmdsdevices : device\n| devices devicedevice : DISPOSITIVO LBRACE NAME RBRACEdevice : DISPOSITIVO LBRACE NAME COMMA NAME RBRACEdevice : DISPOSITIVO COLON LBRACE NAME RBRACEdevice : DISPOSITIVO COLON LBRACE NAME COMMA NAME RBRACEcmds : cmd DOT\n| cmds cmd DOTcmd : attrib\n| obsact\n| act\n| broadcastattrib : SET NAME EQUAL varvar : NUMBERvar : BOOLvar : NAMEobsact : SE condition ENTAOobsact : SE condition ENTAO act\n| SE condition ENTAO act SENAO actcondition : expressionexpression : NAME OPLOGIC varexpression : expression AND expressionact : LIGAR NAMEact : DESLIGAR NAMEact : ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA NAMEact : ENVIAR ALERTA LPAREN MSG RPAREN PARA NAMEact : ENVIAR ALERTA LPAREN MSG RPAREN PARA TODOS COLON name_listact : ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA TODOS COLON name_listbroadcast : ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA TODOS COLON name_listname_list : NAMEname_list : name_list COMMA NAMEact : ENVIAR ALERTA LPAREN MSG RPAREN NAMEact : ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN NAME'
    
_lr_action_items = {'DISPOSITIVO':([0,2,3,6,36,49,55,62,],[4,4,-2,-3,-4,-6,-5,-7,]),'$end':([1,5,20,30,],[0,-1,-8,-9,]),'SET':([2,3,5,6,20,30,36,49,55,62,],[12,-2,12,-3,-8,-9,-4,-6,-5,-7,]),'SE':([2,3,5,6,20,30,36,49,55,62,],[13,-2,13,-3,-8,-9,-4,-6,-5,-7,]),'LIGAR':([2,3,5,6,20,30,32,36,49,51,55,62,],[14,-2,14,-3,-8,-9,14,-4,-6,14,-5,-7,]),'DESLIGAR':([2,3,5,6,20,30,32,36,49,51,55,62,],[15,-2,15,-3,-8,-9,15,-4,-6,15,-5,-7,]),'ENVIAR':([2,3,5,6,20,30,32,36,49,51,55,62,],[16,-2,16,-3,-8,-9,44,-4,-6,44,-5,-7,]),'LBRACE':([4,18,],[17,29,]),'COLON':([4,66,73,82,],[18,70,77,83,]),'DOT':([7,8,9,10,11,19,25,26,32,39,40,41,42,43,57,61,65,68,72,74,75,80,81,84,],[20,-10,-11,-12,-13,30,-24,-25,-18,-17,-14,-15,-16,-19,-20,-33,-27,-34,-26,-28,-31,-29,-32,-29,]),'NAME':([12,13,14,15,17,29,31,33,34,37,50,53,54,60,64,67,69,70,76,77,78,79,83,],[21,24,25,26,28,38,39,24,39,48,56,59,61,65,68,71,72,75,68,75,81,72,75,]),'ALERTA':([16,44,],[27,52,]),'EQUAL':([21,],[31,]),'ENTAO':([22,23,39,41,42,45,46,],[32,-21,-17,-15,-16,-23,-22,]),'AND':([23,39,41,42,45,46,],[33,-17,-15,-16,33,-22,]),'OPLOGIC':([24,],[34,]),'SENAO':([25,26,43,61,65,68,72,74,75,81,84,],[-24,-25,51,-33,-27,-34,-26,-28,-31,-32,-29,]),'LPAREN':([27,52,],[35,58,]),'RBRACE':([28,38,48,56,],[36,49,55,62,]),'COMMA':([28,38,47,63,74,75,80,81,84,],[37,50,53,67,78,-31,78,-32,78,]),'NUMBER':([31,34,],[41,41,]),'BOOL':([31,34,],[42,42,]),'MSG':([35,58,],[47,63,]),'RPAREN':([47,59,63,71,],[54,64,54,76,]),'PARA':([54,64,76,],[60,69,79,]),'TODOS':([60,69,79,],[66,73,82,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'devices':([0,],[2,]),'device':([0,2,],[3,6,]),'cmds':([2,],[5,]),'cmd':([2,5,],[7,19,]),'attrib':([2,5,],[8,8,]),'obsact':([2,5,],[9,9,]),'act':([2,5,32,51,],[10,10,43,57,]),'broadcast':([2,5,],[11,11,]),'condition':([13,],[22,]),'expression':([13,33,],[23,45,]),'var':([31,34,],[40,46,]),'name_list':([70,77,83,],[74,80,84,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> devices cmds','program',2,'p_program','obsact_parser.py',13),
  ('devices -> device','devices',1,'p_devices','obsact_parser.py',54),
  ('devices -> devices device','devices',2,'p_devices','obsact_parser.py',55),
  ('device -> DISPOSITIVO LBRACE NAME RBRACE','device',4,'p_device_simple_nc','obsact_parser.py',64),
  ('device -> DISPOSITIVO LBRACE NAME COMMA NAME RBRACE','device',6,'p_device_obs_nc','obsact_parser.py',72),
  ('device -> DISPOSITIVO COLON LBRACE NAME RBRACE','device',5,'p_device_simple','obsact_parser.py',82),
  ('device -> DISPOSITIVO COLON LBRACE NAME COMMA NAME RBRACE','device',7,'p_device_obs','obsact_parser.py',90),
  ('cmds -> cmd DOT','cmds',2,'p_cmds','obsact_parser.py',100),
  ('cmds -> cmds cmd DOT','cmds',3,'p_cmds','obsact_parser.py',101),
  ('cmd -> attrib','cmd',1,'p_cmd','obsact_parser.py',108),
  ('cmd -> obsact','cmd',1,'p_cmd','obsact_parser.py',109),
  ('cmd -> act','cmd',1,'p_cmd','obsact_parser.py',110),
  ('cmd -> broadcast','cmd',1,'p_cmd','obsact_parser.py',111),
  ('attrib -> SET NAME EQUAL var','attrib',4,'p_attrib','obsact_parser.py',122),
  ('var -> NUMBER','var',1,'p_var_number','obsact_parser.py',133),
  ('var -> BOOL','var',1,'p_var_bool','obsact_parser.py',141),
  ('var -> NAME','var',1,'p_var_name','obsact_parser.py',149),
  ('obsact -> SE condition ENTAO','obsact',3,'p_obsact_empty','obsact_parser.py',157),
  ('obsact -> SE condition ENTAO act','obsact',4,'p_obsact','obsact_parser.py',168),
  ('obsact -> SE condition ENTAO act SENAO act','obsact',6,'p_obsact','obsact_parser.py',169),
  ('condition -> expression','condition',1,'p_condition_expr','obsact_parser.py',185),
  ('expression -> NAME OPLOGIC var','expression',3,'p_expression_cmp','obsact_parser.py',192),
  ('expression -> expression AND expression','expression',3,'p_expression_and','obsact_parser.py',200),
  ('act -> LIGAR NAME','act',2,'p_act_ligar','obsact_parser.py',209),
  ('act -> DESLIGAR NAME','act',2,'p_act_desligar','obsact_parser.py',218),
  ('act -> ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA NAME','act',9,'p_act_alerta_var','obsact_parser.py',227),
  ('act -> ENVIAR ALERTA LPAREN MSG RPAREN PARA NAME','act',7,'p_act_alerta','obsact_parser.py',236),
  ('act -> ENVIAR ALERTA LPAREN MSG RPAREN PARA TODOS COLON name_list','act',9,'p_act_broadcast','obsact_parser.py',245),
  ('act -> ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA TODOS COLON name_list','act',11,'p_act_broadcast_var','obsact_parser.py',258),
  ('broadcast -> ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA TODOS COLON name_list','broadcast',11,'p_broadcast_var','obsact_parser.py',293),
  ('name_list -> NAME','name_list',1,'p_name_list_single','obsact_parser.py',308),
  ('name_list -> name_list COMMA NAME','name_list',3,'p_name_list_rec','obsact_parser.py',316),
  ('act -> ENVIAR ALERTA LPAREN MSG RPAREN NAME','act',6,'p_act_alerta_no_para','obsact_parser.py',324),
  ('act -> ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN NAME','act',8,'p_act_alerta_var_no_para','obsact_parser.py',333),
]
