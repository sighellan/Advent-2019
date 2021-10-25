
def do_add(ll, ii_1, ii_2, ii_3, imme_bool):
    if not imme_bool:
        try:
            ll[ii_3] = ii_1 + ii_2
        except:
            print((ii_1, ii_2, ii_3))
            print(ll)
    return 4
    
def do_mul(ll, ii_1, ii_2, ii_3, imme_bool):
    if not imme_bool:
        ll[ii_3] = ii_1 * ii_2
    return 4

def do_store(ll, ii_1, inp_val, imme_bool):
    if not imme_bool:
        ll[ii_1] = inp_val
    return 2

def do_output(ii_1, verbose):
    if verbose:
        print(ii_1)
    return 2

def jump_if_true(ii_1, ii_2, cur):
    if ii_1:
        return ii_2 
    return cur + 3

def jump_if_false(ii_1, ii_2, cur):
    if not ii_1:
        return ii_2 
    return cur + 3

def do_less_than(ll, ii_1, ii_2, ii_3):
    if ii_1 < ii_2:
        ll[ii_3] = 1
    else:
        ll[ii_3] = 0
    return 4

def do_equals(ll, ii_1, ii_2, ii_3):
    if ii_1 == ii_2:
        ll[ii_3] = 1
    else:
        ll[ii_3] = 0
    return 4

def do_adjust_relative_base(ii_1, rel_index, cur):
    return cur + 2, rel_index + ii_1

def set_up_single(jj, ll, cur, rel_index, pos_code=False):   
    # 0: position mode, use value as pointer
    # 1: immediate mode, use value as int
    # 2: relative mode, use value as pointer with offset
    param = str(ll[cur])[:-2]
    if len(param) >=jj and int(param[len(param)-jj]) == 1: # immediate
        return ll[cur+jj], True
    elif len(param) >=jj and int(param[len(param)-jj]) == 2: # relative
        offset = rel_index
    else:
        offset = 0
    if pos_code:
        assert(cur+jj >= 0)
        return ll[cur+jj]+offset, False
    else:
        assert(cur+jj >= 0)
        assert(ll[cur+jj]+offset >= 0)
        return ll[ll[cur+jj]+offset], False

def set_up_inputs_len_3(ll, cur, rel_index):
    ii_3, imme_bool = set_up_single(3, ll, cur, rel_index, pos_code=True)
    ii_2, _ = set_up_single(2, ll, cur, rel_index)
    ii_1, _ = set_up_single(1, ll, cur, rel_index)
    return ii_1, ii_2, ii_3, imme_bool

def get_inp_val(inp_index, inp_val):
    cur_inp_val = inp_val[inp_index]
    return cur_inp_val, inp_index + 1
    
    
def run_computer(ll, inp_val, verbose=True, out_val=[], 
                 cur=0, inp_index=0, rel_index=0):
    # Provide all inputs so computer can be restarted from previous settings
    
    # Extra memory needs to be provided by appending ll before first starting the computer
    
    while ll[cur] % 100 != 99:
        
        if ll[cur] % 100 == 1:
            ii_1, ii_2, ii_3, imme_bool = set_up_inputs_len_3(ll, cur, rel_index)
            cur = cur + do_add(ll, ii_1, ii_2, ii_3, imme_bool)
        elif ll[cur] % 100 == 2:
            ii_1, ii_2, ii_3, imme_bool = set_up_inputs_len_3(ll, cur, rel_index)
            cur = cur + do_mul(ll, ii_1, ii_2, ii_3, imme_bool)
        elif ll[cur] % 100 == 3:
            if len(inp_val) <= inp_index: # Wait till other machines have run so input is available
                return [cur, inp_index, rel_index], False
            ii_1, imme_bool = set_up_single(1, ll, cur, rel_index, pos_code=True)
            cur_inp_val, inp_index = get_inp_val(inp_index, inp_val)
            cur = cur + do_store(ll, ii_1, cur_inp_val, imme_bool)
        elif ll[cur] % 100 == 4:
            ii_1, imme_bool = set_up_single(1, ll, cur, rel_index, pos_code=False)
            last_output = ii_1
            out_val.append(last_output)
            cur = cur + do_output(ii_1, verbose)
        elif ll[cur] % 100 == 5:
            ii_1, _ = set_up_single(1, ll, cur, rel_index)
            ii_2, _ = set_up_single(2, ll, cur, rel_index)
            cur = jump_if_true(ii_1, ii_2, cur)
        elif ll[cur] % 100 == 6:
            ii_1, _ = set_up_single(1, ll, cur, rel_index)
            ii_2, _ = set_up_single(2, ll, cur, rel_index)
            cur = jump_if_false(ii_1, ii_2, cur)
        elif ll[cur] % 100 == 7:
            ii_1, ii_2, ii_3, imme_bool = set_up_inputs_len_3(ll, cur, rel_index)
            cur = cur + do_less_than(ll, ii_1, ii_2, ii_3)
        elif ll[cur] % 100 == 8:
            ii_1, ii_2, ii_3, imme_bool = set_up_inputs_len_3(ll, cur, rel_index)
            cur = cur + do_equals(ll, ii_1, ii_2, ii_3)
        elif ll[cur] % 100 == 9:
            ii_1, _ = set_up_single(1, ll, cur, rel_index)
            cur, rel_index = do_adjust_relative_base(ii_1, rel_index, cur)
        else:
            print(ll)
            raise ValueError
#     return ll
    return last_output, True
