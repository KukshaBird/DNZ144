from group.models import  Kid

def trans_func(from_k, to_k, responsible_user, amount):

    if from_k == to_k or amount == 0: raise ValueError()
    # if amount provided
    if amount != None:
        if amount > 0:
            committed = list(set(from_k.kids_paid()))
            list_sum = []
            for kid_id in committed:
                kid_obj = Kid.objects.get(id=kid_id)
                kid_balance = from_k.kid_balance(kid_obj)['balance']
                list_sum.append(kid_balance)
            sum_of_list_sum = sum(list_sum)
            for kid_id in committed:
                kid_obj = Kid.objects.get(id=kid_id)
                kid_balance = from_k.kid_balance(kid_obj)['balance']
                quota = kid_balance / sum_of_list_sum
                trans = round(amount * quota, 2)
                if trans != 0:
                    from_k.operations.create(
                        kassa=from_k,
                        kid=kid_obj,
                        amount=trans,
                        user=responsible_user,
                        trans_type="CRE"
                    )
                    to_k.operations.create(
                        kassa=to_k,
                        kid=kid_obj,
                        amount=trans,
                        user=responsible_user,
                        trans_type="DEB"
                    )
            return True
        elif amount < 0:
            for kid_obj in from_k.group.kids.all():
                trans = abs(round(amount / len(from_k.group.kids.all()), 2))
                if trans != 0:
                    from_k.operations.create(
                        kassa=from_k,
                        kid=kid_obj,
                        amount=trans,
                        user=responsible_user,
                        trans_type="DEB"
                    )
                    to_k.operations.create(
                        kassa=to_k,
                        kid=kid_obj,
                        amount=trans,
                        user=responsible_user,
                        trans_type="CRE"
                    )
            return True

    # if not amount
    rest = from_k.get_saldo()
    if rest > 0:
        committed = list(set(from_k.kids_paid()))
        list_sum = []
        for kid_id in committed:
            kid_obj = Kid.objects.get(id=kid_id)
            kid_balance = from_k.kid_balance(kid_obj)['balance']
            list_sum.append(kid_balance)
        sum_of_list_sum = sum(list_sum)
        for kid_id in committed:
            kid_obj = Kid.objects.get(id=kid_id)
            kid_balance = from_k.kid_balance(kid_obj)['balance']
            quota = kid_balance / sum_of_list_sum
            trans = round(rest * quota, 2)
            if trans != 0:
                from_k.operations.create(
                    kassa=from_k,
                    kid=kid_obj,
                    amount=trans,
                    user=responsible_user,
                    trans_type="CRE"
                )
                to_k.operations.create(
                    kassa=to_k,
                    kid=kid_obj,
                    amount=trans,
                    user=responsible_user,
                    trans_type="DEB"
                )
        return True
    if rest < 0:
        for kid_obj in from_k.group.kids.all():
            trans = abs(round(rest / len(from_k.group.kids.all()), 2))
            if trans != 0:
                from_k.operations.create(
                    kassa=from_k,
                    kid=kid_obj,
                    amount=trans,
                    user=responsible_user,
                    trans_type="DEB"
                )
                to_k.operations.create(
                    kassa=to_k,
                    kid=kid_obj,
                    amount=trans,
                    user=responsible_user,
                    trans_type="CRE"
                )
        return True
    raise ValueError()
