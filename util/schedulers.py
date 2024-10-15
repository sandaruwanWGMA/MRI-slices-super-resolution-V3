from torch.nn import init
from torch.optim import lr_scheduler


def get_scheduler(optimizer, opt):
    """Return a learning rate scheduler

    Parameters:
        optimizer          -- the optimizer of the network
        opt (dict)         -- dictionary containing all the experiment flags
                              opt["lr_policy"] is the name of learning rate policy: linear | step | plateau | cosine
    """
    if opt["lr_policy"] == "linear":

        def lambda_rule(epoch):
            lr_l = 1.0 - max(0, epoch + opt["epoch_count"] - opt["n_epochs"]) / float(
                opt["n_epochs_decay"] + 1
            )
            return lr_l

        scheduler = lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda_rule)
    elif opt["lr_policy"] == "step":
        scheduler = lr_scheduler.StepLR(
            optimizer, step_size=opt["lr_decay_iters"], gamma=0.1
        )
    elif opt["lr_policy"] == "plateau":
        scheduler = lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="min", factor=0.2, threshold=0.01, patience=5
        )
    elif opt["lr_policy"] == "cosine":
        scheduler = lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=opt["n_epochs"], eta_min=0
        )
    else:
        return NotImplementedError(
            f"learning rate policy [{opt['lr_policy']}] is not implemented"
        )
    return scheduler
